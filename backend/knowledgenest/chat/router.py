from typing import List
from fastapi import APIRouter, WebSocket
from knowledgenest.database import DbSession
from knowledgenest.auth.service import CurrentUser, curr_user
from knowledgenest.chat.schema import (
    ChatConversationOut,
    ChatMessageIn,
    ChatMessageOut,
    FirstChatMessageOut,
)
from knowledgenest.chat.service import (
    chat,
    add_conversation,
    chat_stream,
    fetch_conversation,
    fetch_conversations,
)


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=FirstChatMessageOut)
def create_convesation(
    request: ChatMessageIn, current_user: CurrentUser, db: DbSession
):
    conversation = add_conversation(current_user.id, db)
    conversation_id = str(conversation.id)
    message = chat(request.message, conversation_id, current_user.id, db)
    return dict(message=message, type="ai", conversation_id=conversation.id)


@router.get("/", response_model=List[ChatConversationOut])
def get_conversations(current_user: CurrentUser, db: DbSession):
    conversations = fetch_conversations(current_user.id, db)
    formatted_conversations = [
        ChatConversationOut(id=conversation.id, name=conversation.name)
        for conversation in conversations
    ]
    return formatted_conversations


@router.get("/{id}", response_model=List[ChatMessageOut])
def get_conversation(id: str, current_user: CurrentUser, db: DbSession):
    messages = fetch_conversation(id, current_user.id, db)
    formatted_messages = [
        ChatMessageOut(message=msg.content, type=msg.type) for msg in messages
    ]
    return formatted_messages


@router.post("/{id}", response_model=ChatMessageOut)
def send_chat(
    id: str, request: ChatMessageIn, current_user: CurrentUser, db: DbSession
):
    message = chat(request.message, id, current_user.id, db)
    return ChatMessageOut(message=message, type="ai")


@router.websocket("/{id}/ws")
async def websocket_endpoint(id: str, token: str, db: DbSession, websocket: WebSocket):
    try:
        user = curr_user(db, token)
        await websocket.accept()
        while True:
            message = await websocket.receive_text()
            await websocket.send_text("<START>")
            async for token in chat_stream(message, id, str(user.id), db):
                await websocket.send_text(token)

    except Exception as e:
        print(e)
