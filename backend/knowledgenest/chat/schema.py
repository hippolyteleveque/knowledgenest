from pydantic import BaseModel, UUID4


class ChatMessageIn(BaseModel):
    message: str


class ChatMessageOut(BaseModel):
    message: str
    type: str


class FirstChatMessageOut(BaseModel):
    message: str
    type: str
    conversation_id: UUID4


class ChatConversationOut(BaseModel):
    id: UUID4
    name: str
