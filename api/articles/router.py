from fastapi import APIRouter

from api.articles.schema import ArticleUrlIn
from api.auth.service import CurrentUser


router = APIRouter(prefix="/articles", tags=["articles"])


@router.post("/")
def add_article(request: ArticleUrlIn, current_user: CurrentUser):
    # TODO : add article in the db
    return {
        "message": f"Article {request.url} has been added for user {current_user.email}"
    }
