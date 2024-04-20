from typing import List
from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_204_NO_CONTENT

from api.articles.schema import ArticleOut, ArticleUrlIn
from api.articles.service import (
    delete_article_by_id,
    fetch_all_articles,
    process_new_article,
)
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


@router.delete("/{id}")
def delete_article(id: int, current_user: CurrentUser, db: DbSession):
    _ = delete_article_by_id(id, current_user.id, db)
    return HTTPException(status_code=HTTP_204_NO_CONTENT)
