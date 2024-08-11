from sqlalchemy import Column, ForeignKey, String, DateTime
from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from knowledgenest.database import Base


class ChatConversation(Base):
    __tablename__ = "chatconversation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime)

    # relationships
    messages = relationship("ChatMessage", back_populates="conversation")


class ChatMessage(Base):
    __tablename__ = "chatmessage"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime)
    content = Column(String)
    type = Column(String)

    # relationships
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("chatconversation.id"))
    conversation = relationship("ChatConversation", back_populates="messages")

    def convert_to_langchain(self):
        if self.type == "human":
            return HumanMessage(self.content)
        return AIMessage(self.content)
