from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from knowledgenest.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # relations
    conversations = relationship("ChatConversation", back_populates="user")