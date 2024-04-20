from pydantic import BaseModel


class ArticleUrlIn(BaseModel):
    url: str
