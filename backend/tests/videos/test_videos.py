import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid
from datetime import date

from knowledgenest.videos.models import Video
from knowledgenest.videos.router import add_video, delete_video, get_videos
from knowledgenest.videos.schema import VideoUrlIn
from knowledgenest.videos.service import process_new_video, delete_video_by_id, fetch_videos
from knowledgenest.videos.utils import extract_info_from_url

# Test router functions


def test_get_videos(authorized_client, db_session, test_created_user, auth_headers):
    # Add some test videos to the database
    for i in range(3):
        video = Video(
            title=f"Test Video {i}",
            url=f"https://youtube.com/watch?v=test{i}",
            imageUrl=f"https://img.youtube.com/vi/test{i}/0.jpg",
            description=f"Test video {i}",
            publishDate=date.today(),
            author="Test Author",
            user_id=test_created_user["id"])
        db_session.add(video)
    db_session.commit()

    response = authorized_client.get("/videos/")
    assert response.status_code == 200
    data = response.json()
    assert data["videos_count"] == 3
    assert len(data["videos"]) == 3


def test_add_video(authorized_client, db_session, test_created_user, mock_pinecone):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    mock_video = Video(
        title="Test Title",
        description="Test Description",
        url=url,
        id=uuid.uuid4(),
        imageUrl="https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg",
        publishDate=date.today(),
        author="Test Author",
        user_id=test_created_user["id"]
    )

    with patch("knowledgenest.videos.router.process_new_video") as mock_process, \
            patch("fastapi.BackgroundTasks.add_task") as mock_add_task:
        mock_process.return_value = mock_video
        response = authorized_client.post("/videos/", json={"url": url})
        mock_process.assert_called_once_with(
            url, test_created_user["id"], db_session)
        mock_add_task.assert_called_once()
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == url
        assert data["id"] == str(mock_video.id)
        assert data["title"] == mock_video.title
        assert data["description"] == mock_video.description
        assert data["imageUrl"] == mock_video.imageUrl


def test_delete_video(authorized_client, db_session, test_created_user, mock_pinecone):
    # Add a test video
    user_id = test_created_user["id"]
    video = Video(
        title="Test Video",
        url="https://youtube.com/watch?v=test",
        imageUrl="https://img.youtube.com/vi/test/0.jpg",
        description="Test video",
        publishDate=date.today(),
        author="Test Author",
        user_id=user_id)
    db_session.add(video)
    db_session.commit()

    with patch("knowledgenest.videos.router.delete_video_chunks_by_id") as mock_delete_chunks:
        response = authorized_client.delete(f"/videos/{video.id}")
        assert response.status_code == 204
        mock_delete_chunks.assert_called_once()

    # Verify the video is deleted from the database
    deleted_video = db_session.query(
        Video).filter(Video.id == video.id).first()
    assert deleted_video is None

# Test service functions


def test_process_new_video(db_session, test_created_user):
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    user_id = test_created_user["id"]

    with patch("knowledgenest.videos.service.extract_info_from_url") as mock_extract:
        mock_extract.return_value = {
            "title": "Test Title",
            "description": "Test Description",
            "imageUrl": "https://img.youtube.com/vi/dQw4w9WgXcQ/0.jpg",
            "publishDate": date.today(),
            "author": "Test Author"
        }

        video = process_new_video(url, user_id, db_session)
        mock_extract.assert_called_once_with(url)
        assert video.url == url
        assert video.user_id == user_id
        assert video.title == "Test Title"
        assert video.description == "Test Description"


def test_fetch_videos(db_session, test_created_user):
    user_id = test_created_user["id"]
    for i in range(5):
        video = Video(
            title=f"Test Video {i}",
            url=f"https://youtube.com/watch?v=test{i}",
            imageUrl=f"https://img.youtube.com/vi/test{i}/0.jpg",
            description=f"Test video {i}",
            publishDate=date.today(),
            author="Test Author",
            user_id=user_id)
        db_session.add(video)
    db_session.commit()

    result = fetch_videos(user_id, db_session, offset=1, limit=2)
    assert result["videos_count"] == 5
    assert len(result["videos"]) == 2


def test_delete_video_by_id(db_session, test_created_user):
    user_id = test_created_user["id"]
    video = Video(
        title="Test Video",
        url="https://youtube.com/watch?v=test",
        imageUrl="https://img.youtube.com/vi/test/0.jpg",
        description="Test video",
        publishDate=date.today(),
        author="Test Author",
        user_id=user_id)
    db_session.add(video)
    db_session.commit()

    deleted_video = delete_video_by_id(video.id, user_id, db_session)
    assert deleted_video.id == video.id

    with pytest.raises(HTTPException):
        delete_video_by_id(video.id, user_id, db_session)
