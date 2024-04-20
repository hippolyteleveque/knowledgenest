from pydantic import BaseModel


class ArticleUrlIn(BaseModel):
    url: str


class ArticleOut(BaseModel):
    url: str
    imageUrl: str
    description: str
    title: str
