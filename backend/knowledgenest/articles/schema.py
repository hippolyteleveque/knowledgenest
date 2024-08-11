from typing import List
from uuid import UUID
from pydantic import BaseModel


class ArticleUrlIn(BaseModel):
    url: str


class ArticleOut(BaseModel):
    id: UUID
    url: str
    imageUrl: str
    description: str
    title: str


class ArticlesOut(BaseModel):
    articles: List[ArticleOut]
    articles_count: int
