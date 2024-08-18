from typing import List
from sqlalchemy import and_, desc
from sqlalchemy.orm.session import Session


from knowledgenest.chat.models import ChatConversation, ChatMessage
from knowledgenest.chat.utils import get_chain
from datetime import datetime


def fetch_conversation(
    conversation_id: str, user_id: str, db: Session
) -> List[ChatMessage]:
    conversation = (
        db.query(ChatConversation)
        .filter(
            and_(
                ChatConversation.id == conversation_id,
                ChatConversation.user_id == user_id,
            )
        )
        .first()
    )
    if conversation:
        return conversation.ordered_messages
    return []


def fetch_conversations(user_id: str, db: Session) -> List[ChatConversation]:
    conversations = (
        db.query(ChatConversation)
        .filter(ChatConversation.user_id == user_id)
        .order_by(desc(ChatConversation.created_at))
        .all()
    )
    return conversations


def chat(new_message: str, conversation_id: str, user_id: str, db: Session) -> str:
    """Continue the chat with the user"""
    add_human_message(new_message, conversation_id, db)
    db_conversation = fetch_conversation(conversation_id, user_id, db)
    messages = [msg.convert_to_langchain() for msg in db_conversation]
    chain = get_chain()
    resp = chain.invoke(dict(messages=messages))
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


def add_conversation(user_id: str, db: Session):
    """Create a new conversation"""
    new_conversation = ChatConversation(user_id=user_id, created_at=datetime.now())
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation
