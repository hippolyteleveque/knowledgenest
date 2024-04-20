from typing import List
from fastapi import APIRouter

from api.articles.schema import ArticleOut, ArticleUrlIn
from api.articles.service import fetch_all_articles, process_new_article
from api.auth.service import CurrentUser
from api.database import DbSession


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=List[ArticleOut])
def get_articles(current_user: CurrentUser, db: DbSession):
    # TODO handle pagination
    all_articles = fetch_all_articles(current_user.id, db)
    return all_articles


@router.post("/", response_model=ArticleOut)
def add_article(request: ArticleUrlIn, current_user: CurrentUser, db: DbSession):
    new_article = process_new_article(request.url, current_user.id, db)
    return new_article
