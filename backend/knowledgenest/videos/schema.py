from typing import List
from uuid import UUID
from pydantic import BaseModel


class VideoUrlIn(BaseModel):
    url: str


class VideoOut(BaseModel):
    id: UUID
    url: str
    imageUrl: str
    description: str
    title: str


class VideosOut(BaseModel):
    videos: List[VideoOut]
    videos_count: int
