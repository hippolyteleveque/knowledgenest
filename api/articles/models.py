from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    url = Column(String, index=True)
    description = Column(String)
    imageUrl = Column(String)
    title = Column(String)

    # relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
