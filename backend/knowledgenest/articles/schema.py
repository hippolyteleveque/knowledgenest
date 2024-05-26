from typing import List
from pydantic import BaseModel


class ArticleUrlIn(BaseModel):
    url: str


class ArticleOut(BaseModel):
    id: int
    url: str
    imageUrl: str
    description: str
    title: str


class ArticlesOut(BaseModel):
    articles: List[ArticleOut]
    articles_count: int
