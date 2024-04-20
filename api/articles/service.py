from sqlalchemy.orm.session import Session
from fastapi import HTTPException
from api.articles.models import Article
from api.articles.utils import convert_properties_to_fields, extract_meta_properties
from starlette.status import HTTP_404_NOT_FOUND


def process_new_article(url, user_id: int, db: Session):
    # First version, we only create the article in base,
    properties = extract_meta_properties(url)
    fields = convert_properties_to_fields(properties)
    new_article = Article(**fields, user_id=user_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article


def fetch_all_articles(user_id: int, db: Session):
    return db.query(Article).filter(Article.user_id == user_id).all()


def delete_article_by_id(article_id: int, user_id: int, db: Session):
    article = (
        db.query(Article)
        .filter(Article.id == article_id, Article.user_id == user_id)
        .first()
    )
    if not article:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    db.delete(article)
    db.commit()
    return article
