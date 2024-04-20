from sqlalchemy.orm.session import Session
from api.articles.models import Article


def process_new_article(url, user_id: int, db: Session):
    # First version, we only create the article in base,
    new_article = Article(url=url, user_id=user_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article
