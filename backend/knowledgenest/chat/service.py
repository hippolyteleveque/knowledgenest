import os
from sqlalchemy import asc
from sqlalchemy.orm.session import Session
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from knowledgenest.chat.models import ChatMessage

from datetime import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"


def send_llm_message(message: str) -> str:
    """Simple llm invocation of OPENAI llm"""

    llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY)
    chain = llm | StrOutputParser()
    resp = chain.invoke(message)
    return resp


def chat(new_message: str, db: Session) -> str:
    """Continue the chat with the user"""
    add_human_message(new_message, db)
    db_messages = db.query(ChatMessage).order_by(asc(ChatMessage.created_at)).all()
    messages = [msg.convert_to_langchain() for msg in db_messages]
    print(messages)
    llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY)
    chain = llm | StrOutputParser()
    resp = chain.invoke(messages)
    add_ai_message(resp, db)
    return resp


def add_human_message(content: str, db: Session):
    new_message = ChatMessage(content=content, type="human", created_at=datetime.now())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def add_ai_message(content: str, db: Session):
    new_message = ChatMessage(content=content, type="ai", created_at=datetime.now())
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message
