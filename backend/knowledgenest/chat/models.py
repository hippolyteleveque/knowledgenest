from sqlalchemy import Column, ForeignKey, String, DateTime, Float
from langchain_core.messages import AIMessage, HumanMessage
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from knowledgenest.database import Base


class ChatConversation(Base):
    __tablename__ = "chatconversation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime)

    @property
    def name(self):
        return self.messages[0].content[:25]

    @property
    def ordered_messages(self):
        return sorted(self.messages, key=lambda x: x.created_at)

    # relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation")
    articles = relationship("Article", secondary="conversation_context_article")
    videos = relationship("Video", secondary="conversation_context_video")
    context_articles = relationship(
        "ConversationContextArticle", back_populates="conversation", viewonly=True
    )
    context_videos = relationship(
        "ConversationContextVideo", back_populates="conversation", viewonly=True
    )


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


class ConversationContextArticle(Base):
    __tablename__ = "conversation_context_article"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score = Column(Float)

    # relations
    article_id = Column(UUID(as_uuid=True), ForeignKey("articles.id"))
    article = relationship("Article")
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("chatconversation.id"))
    conversation = relationship("ChatConversation", back_populates="context_articles")


class ConversationContextVideo(Base):
    __tablename__ = "conversation_context_video"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score = Column(Float)

    # relations
    video_id = Column(UUID(as_uuid=True), ForeignKey("videos.id"))
    video = relationship("Video")
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("chatconversation.id"))
    conversation = relationship("ChatConversation", back_populates="context_videos")
