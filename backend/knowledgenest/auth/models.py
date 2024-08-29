from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String

# from sqlalchemy.dialects.postgresql import UUID
from knowledgenest.database import Base
import uuid
from uuid import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# prevent IDE and code checkers errors
if TYPE_CHECKING:
    from knowledgenest.chat.models import ChatConversation


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)

    # relations
    setting: Mapped["UserSetting"] = relationship(back_populates="user")
    conversations: Mapped[list["ChatConversation"]] = relationship(
        back_populates="user"
    )


class UserSetting(Base):
    __tablename__ = "user_settings"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    ai_provider: Mapped[str] = mapped_column(String, default="mistral")

    # relations
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="setting")
