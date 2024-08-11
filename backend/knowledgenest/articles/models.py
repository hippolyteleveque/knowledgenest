from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from knowledgenest.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url = Column(String, index=True)
    description = Column(String)
    imageUrl = Column(String)
    title = Column(String)

    # relationships
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    user = relationship("User")
