from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from knowledgenest.database import Base

# prevent IDE and code checkers errors
if TYPE_CHECKING:
    from knowledgenest.auth.models import User


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    url: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    imageUrl: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)

    # relationships
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )
    user: Mapped["User"] = relationship("User")
