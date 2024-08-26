from typing import List
from uuid import UUID
from sqlalchemy import and_, desc
from sqlalchemy.orm.session import Session


from knowledgenest.chat.models import ConversationContextArticle
from knowledgenest.chat.models import ConversationContextVideo
from knowledgenest.chat.models import ChatConversation, ChatMessage
from knowledgenest.chat.utils import get_chain
from datetime import datetime


def fetch_conversation(
    conversation_id: str, user_id: str, db: Session
) -> ChatConversation:
    """Fetch a specific conversation"""
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
    if not conversation:
        raise ValueError(f"Conversation with id {id} does not exists.")
    return conversation


def fetch_conversations(user_id: str, db: Session) -> List[ChatConversation]:
    """Returns all conversations of the user"""
    conversations = (
        db.query(ChatConversation)
        .filter(ChatConversation.user_id == user_id)
        .order_by(desc(ChatConversation.created_at))
        .all()
    )
    return conversations


async def chat_stream(
    new_message: str, conversation_id: str, user_id: str, db: Session
):
    """Continue the chat with the user on the specified conversation"""
    if new_message != "<START>":  # TODO change this
        add_human_message(new_message, conversation_id, db)
    db_conversation = fetch_conversation(conversation_id, user_id, db)
    messages = [msg.convert_to_langchain() for msg in db_conversation.ordered_messages]
    chain = get_chain(str(user_id))
    resp = chain.astream(dict(messages=messages))
    total_message = ""
    async for chunk in resp:
        if "sources" in chunk:
            # Add all sources to the conversation
            for source in chunk["sources"]:
                add_new_source(
                    conversation_id, source["id"], source["type"], source["score"], db
                )
        elif "output" in chunk:
            total_message += chunk["output"]
            yield chunk
    add_ai_message(total_message, conversation_id, db)


def add_human_message(content: str, conversation_id: str, db: Session) -> ChatMessage:
    """Record a new Human message in the db"""
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


def add_ai_message(content: str, conversation_id: str, db: Session) -> ChatMessage:
    """Add a new AI message on the database"""
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


def add_conversation(user_id: str, db: Session) -> ChatConversation:
    """Create a new conversation"""
    new_conversation = ChatConversation(user_id=user_id, created_at=datetime.now())
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation


def add_new_source(
    conversation_id: UUID, source_id: UUID, source_type: str, score: float, db: Session
) -> None:
    """Add a new source to the conversation id"""
    if source_type == "video":
        new_source = ConversationContextVideo(
            conversation_id=conversation_id, video_id=source_id, score=score
        )
    elif source_type == "article":
        new_source = ConversationContextArticle(
            conversation_id=conversation_id, article_id=source_id, score=score
        )
    else:
        raise TypeError(f"Source type not known : {source_type}")
    db.add(new_source)
    db.commit()


def fetch_sources(conversation_id: UUID, current_user_id: UUID, db: Session):
    conversation = fetch_conversation(conversation_id, current_user_id, db)
    videos_map = {}
    # we only get the best score
    for ctx in conversation.context_videos:
        videos_map[ctx.video_id] = {"score": ctx.score}
    for video in conversation.videos:
        videos_map[video.id].update(
            {
                "id": video.id,
                "imageUrl": video.imageUrl,
                "title": video.title,
                "description": video.description,
                "url": video.url,
            }
        )
    articles_map = {}
    # we only get the best score
    for ctx in conversation.context_articles:
        articles_map[ctx.article_id] = {"score": ctx.score}
    for article in conversation.articles:
        articles_map[article.id].update(
            {
                "id": article.id,
                "imageUrl": article.imageUrl,
                "title": article.title,
                "description": article.description,
                "url": article.url,
            }
        )
    return list(videos_map.values()), list(articles_map.values())
