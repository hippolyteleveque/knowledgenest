from sqlalchemy.orm.session import Session
from api.articles.models import Article
from api.articles.utils import convert_properties_to_fields, extract_meta_properties


def process_new_article(url, user_id: int, db: Session):
    # First version, we only create the article in base,
    properties = extract_meta_properties(url)
    fields = convert_properties_to_fields(properties)
    new_article = Article(**fields, user_id=user_id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article
