from sqlalchemy import ForeignKey, String, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from langchain_core.messages import AIMessage, HumanMessage
import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from knowledgenest.database import Base

# prevent IDE and code checkers errors
if TYPE_CHECKING:
    from knowledgenest.auth.models import User
    from knowledgenest.articles.models import Article
    from knowledgenest.videos.models import Video


class ChatConversation(Base):
    __tablename__ = "chatconversation"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(DateTime)

    @property
    def name(self):
        return self.messages[0].content[:25]

    @property
    def ordered_messages(self):
        return sorted(self.messages, key=lambda x: x.created_at)

    # relationships
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    user: Mapped["User"] = relationship("User", back_populates="conversations")
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="conversation"
    )
    articles: Mapped[list["Article"]] = relationship(
        secondary="conversation_context_article"
    )
    videos: Mapped[list["Video"]] = relationship(secondary="conversation_context_video")
    context_articles: Mapped[list["ConversationContextArticle"]] = relationship(
        "ConversationContextArticle", back_populates="conversation", viewonly=True
    )
    context_videos: Mapped[list["ConversationContextVideo"]] = relationship(
        "ConversationContextVideo", back_populates="conversation", viewonly=True
    )


class ChatMessage(Base):
    __tablename__ = "chatmessage"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(DateTime)
    content: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

    # relationships
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chatconversation.id")
    )
    conversation: Mapped["ChatConversation"] = relationship(
        "ChatConversation", back_populates="messages"
    )

    def convert_to_langchain(self):
        if self.type == "human":
            return HumanMessage(self.content)
        return AIMessage(self.content)


class ConversationContextArticle(Base):
    __tablename__ = "conversation_context_article"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    score: Mapped[float] = mapped_column(Float)

    # relations
    article_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("articles.id")
    )
    article: Mapped["Article"] = relationship("Article", overlaps="articles")
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chatconversation.id")
    )
    conversation: Mapped["ChatConversation"] = relationship(
        "ChatConversation", back_populates="context_articles", overlaps="articles"
    )


class ConversationContextVideo(Base):
    __tablename__ = "conversation_context_video"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    score: Mapped[float] = mapped_column(Float)

    # relations
    video_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("videos.id")
    )
    video: Mapped["Video"] = relationship("Video", overlaps="videos")
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chatconversation.id")
    )
    conversation: Mapped["ChatConversation"] = relationship(
        "ChatConversation", back_populates="context_videos", overlaps="videos"
    )
