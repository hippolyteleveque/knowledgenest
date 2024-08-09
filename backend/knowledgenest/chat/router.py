from fastapi import APIRouter
from knowledgenest.database import DbSession
from knowledgenest.chat.schema import ChatMessageIn, ChatMessageOut
from knowledgenest.chat.service import chat


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatMessageOut)
def send_message(request: ChatMessageIn, db: DbSession):
    message = chat(request.message, db)
    return ChatMessageOut(message=message)
