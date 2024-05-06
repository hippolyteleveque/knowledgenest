from fastapi import APIRouter, HTTPException, BackgroundTasks
from starlette.status import HTTP_204_NO_CONTENT

from api.articles.schema import ArticleOut, ArticleUrlIn, ArticlesOut
from api.articles.service import (
    delete_article_by_id,
    delete_article_chunks_by_id,
    embed_and_ingest_article,
    fetch_articles,
    process_new_article,
)
from api.auth.service import CurrentUser
from api.database import DbSession
from api.vector_database import VectorDbSession


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=ArticlesOut)
def get_articles(
    current_user: CurrentUser, db: DbSession, offset: int = 0, limit: int = 10
):
    # TODO handle pagination
    all_articles = fetch_articles(current_user.id, db, offset, limit)
    return all_articles


@router.post("/", response_model=ArticleOut)
def add_article(
    request: ArticleUrlIn,
    current_user: CurrentUser,
    db: DbSession,
    index: VectorDbSession,
    background_tasks: BackgroundTasks,
):
    new_article = process_new_article(request.url, current_user.id, db)
    # Chunk and embed the article as a background task
    background_tasks.add_task(embed_and_ingest_article, new_article, index)
    return new_article


@router.delete("/{id}")
def delete_article(
    id: int, current_user: CurrentUser, db: DbSession, index: VectorDbSession
):
    _ = delete_article_by_id(id, current_user.id, db)
    # You need to wait before it is actually processed before effectively deleting the vectors
    delete_article_chunks_by_id(id, index)
    return HTTPException(status_code=HTTP_204_NO_CONTENT)
