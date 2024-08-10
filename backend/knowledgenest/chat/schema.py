from pydantic import BaseModel


class ChatMessageIn(BaseModel):
    message: str


class ChatMessageOut(BaseModel):
    message: str
    type: str


class FirstChatMessageOut(BaseModel):
    message: str
    type: str
    conversation_id: int


class ChatConversationOut(BaseModel):
    id: int
