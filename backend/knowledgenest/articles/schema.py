from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class ArticleUrlIn(BaseModel):
    url: str


class ArticleOut(BaseModel):
    id: UUID
    url: str
    imageUrl: Optional[str]
    description: Optional[str]
    title: str


class ArticlesOut(BaseModel):
    articles: List[ArticleOut]
    articles_count: int
