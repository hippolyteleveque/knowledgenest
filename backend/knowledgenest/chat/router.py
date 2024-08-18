from typing import List
from fastapi import APIRouter
from knowledgenest.database import DbSession
from knowledgenest.auth.service import CurrentUser
from knowledgenest.chat.schema import (
    ChatConversationOut,
    ChatMessageIn,
    ChatMessageOut,
    FirstChatMessageOut,
)
from knowledgenest.chat.service import (
    chat,
    add_conversation,
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
