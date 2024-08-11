import os
from typing import List
from sqlalchemy import asc
from sqlalchemy.orm.session import Session
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from knowledgenest.chat.models import ChatConversation, ChatMessage

from datetime import datetime

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"


def send_llm_message(message: str) -> str:
    """Simple llm invocation of OPENAI llm"""

    llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY)
    chain = llm | StrOutputParser()
    resp = chain.invoke(message)
    return resp


def fetch_conversation(conversation_id: str, db: Session) -> List[ChatMessage]:
    db_conversation = (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(asc(ChatMessage.created_at))
        .all()
    )
    return db_conversation


def fetch_conversations(db: Session) -> List[ChatConversation]:
    conversations = (
        db.query(ChatConversation).order_by(asc(ChatConversation.created_at)).all()
    )
    return conversations


def chat(new_message: str, conversation_id: str, db: Session) -> str:
    """Continue the chat with the user"""
    add_human_message(new_message, conversation_id, db)
    db_conversation = fetch_conversation(conversation_id, db)
    messages = [msg.convert_to_langchain() for msg in db_conversation]
    llm = ChatOpenAI(model=MODEL, api_key=OPENAI_API_KEY)
    chain = llm | StrOutputParser()
    resp = chain.invoke(messages)
    add_ai_message(resp, conversation_id, db)
    return resp


def add_human_message(content: str, conversation_id: str, db: Session):
    new_message = ChatMessage(
        content=content,
        type="human",
        created_at=datetime.now(),
        conversation_id=conversation_id,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def add_ai_message(content: str, conversation_id: str, db: Session):
    new_message = ChatMessage(
        content=content,
        type="ai",
        created_at=datetime.now(),
        conversation_id=conversation_id,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message


def add_conversation(db: Session):
    """Create a new conversation"""
    new_conversation = ChatConversation(created_at=datetime.now())
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation
