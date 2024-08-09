from sqlalchemy import Column, Integer, String, DateTime
from langchain_core.messages import AIMessage, HumanMessage

from knowledgenest.database import Base


class ChatMessage(Base):
    __tablename__ = "chatmessage"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    content = Column(String)
    type = Column(String)

    def convert_to_langchain(self):
        if self.type == "human":
            return HumanMessage(self.content)
        return AIMessage(self.content)
