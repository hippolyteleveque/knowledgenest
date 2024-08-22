from fastapi import APIRouter, BackgroundTasks, HTTPException
from starlette.status import HTTP_204_NO_CONTENT

from knowledgenest.videos.schema import VideoOut, VideoUrlIn, VideosOut
from knowledgenest.videos.service import (
    delete_video_by_id,
    delete_video_chunks_by_id,
    embed_ang_ingest_video,
    fetch_videos,
    process_new_video,
)
from knowledgenest.auth.service import CurrentUser
from knowledgenest.database import DbSession
from knowledgenest.vector_database import VectorDbSession

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("/", response_model=VideosOut)
def get_videos(
    current_user: CurrentUser, db: DbSession, offset: int = 0, limit: int = 0
):
    videos = fetch_videos(str(current_user.id), db, offset, limit)
    return videos


@router.post("/", response_model=VideoOut)
def add_video(
    request: VideoUrlIn,
    current_user: CurrentUser,
    db: DbSession,
    index: VectorDbSession,
    background_tasks: BackgroundTasks,
):
    new_video = process_new_video(request.url, str(current_user.id), db)
    background_tasks.add_task(embed_ang_ingest_video, new_video, index)
    return new_video


@router.delete("/{id}")
def delete_video(
    id: str,
    current_user: CurrentUser,
    db: DbSession,
    index: VectorDbSession,
    background_tasks: BackgroundTasks,
):
    delete_video_by_id(id, str(current_user.id), db)
    delete_video_chunks_by_id(id, index)
    return HTTPException(status_code=HTTP_204_NO_CONTENT)
