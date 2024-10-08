from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, WebSocket
from knowledgenest.database import DbSession
from knowledgenest.auth.service import CurrentUser, curr_user
from knowledgenest.chat.schema import (
    ChatConversationOut,
    ChatMessageIn,
    ChatMessageOut,
)
from knowledgenest.chat.service import (
    add_human_message,
    add_conversation,
    chat_stream,
    fetch_conversation,
    fetch_conversations,
    fetch_sources,
)


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatConversationOut)
def create_conversation(
    request: ChatMessageIn, current_user: CurrentUser, db: DbSession
):
    conversation = add_conversation(current_user.id, db)
    add_human_message(request.message, conversation.id, db)
    db.refresh(conversation)  # so that it has the messages
    return conversation


@router.get("/", response_model=List[ChatConversationOut])
def get_conversations(current_user: CurrentUser, db: DbSession):
    # TODO handle pagination
    conversations = fetch_conversations(current_user.id, db)
    return conversations


@router.get("/{id}", response_model=List[ChatMessageOut])
def get_conversation(id: str, current_user: CurrentUser, db: DbSession):
    conversation = fetch_conversation(id, current_user.id, db)
    messages = conversation.ordered_messages
    formatted_messages = [
        ChatMessageOut(message=msg.content, type=msg.type) for msg in messages
    ]
    return formatted_messages


@router.get("/{id}/sources")
def get_conversation_sources(id: UUID, current_user: CurrentUser, db: DbSession):
    videos, articles = fetch_sources(id, current_user.id, db)
    return dict(videos=videos, articles=articles)


@router.websocket("/{id}/ws")
async def websocket_endpoint(id: UUID, token: str, db: DbSession, websocket: WebSocket):
    try:
        user = curr_user(db, token)
        await websocket.accept()
        while True:
            message = await websocket.receive_text()
            send_start = True
            stream = chat_stream(message, id, user, db)

            async for chunk in stream:
                if send_start:
                    await websocket.send_text("<START>")
                    send_start = False
                await websocket.send_json(chunk)
    except Exception as e:
        # await websocket.close()
        raise HTTPException(
            status_code=500, detail=f"The following error occurred: {e}"
        )
