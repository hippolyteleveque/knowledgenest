from fastapi import APIRouter
from knowledgenest.chat.schema import ChatMessageIn, ChatMessageOut
from knowledgenest.chat.service import send_llm_message


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/", response_model=ChatMessageOut)
def send_message(request: ChatMessageIn):
    message = send_llm_message(request.message)
    return ChatMessageOut(message=message)
