import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from sqlalchemy.orm import Session
import uuid

from knowledgenest.articles.models import Article
from knowledgenest.articles.router import add_article, delete_article, get_articles
from knowledgenest.articles.schema import ArticleUrlIn
from knowledgenest.articles.service import process_new_article, delete_article_by_id, fetch_articles
from knowledgenest.articles.utils import extract_meta_properties, convert_properties_to_fields

# Test router functions


def test_get_articles(authorized_client, db_session, test_created_user, auth_headers):
    # Add some test articles to the database
    for i in range(3):
        article = Article(
            title=f"Test Article {i}",
            url=f"http://test{i}.com",
            imageUrl=f"http://test.com/{i}",
            description=f"Test article {i}",
            user_id=test_created_user["id"])
        db_session.add(article)
    db_session.commit()
    response = authorized_client.get("/articles/")
    assert response.status_code == 200
    data = response.json()
    assert data["articles_count"] == 3
    assert len(data["articles"]) == 3


def test_add_article(authorized_client, db_session, test_created_user, mock_pinecone):
    url = "http://example.com"
    mock_article = Article(
        title="Test Title",
        description="Test Description",
        url=url,
        id=uuid.uuid4(),
        imageUrl="http://example.com/image",
        user_id=test_created_user["id"]
    )

    with patch("knowledgenest.articles.router.process_new_article") as mock_process, \
            patch("fastapi.BackgroundTasks.add_task") as mock_add_task:
        mock_process.return_value = mock_article
        response = authorized_client.post("/articles/", json={"url": url})
        mock_process.assert_called_once_with(
            url, test_created_user["id"], db_session)
        mock_add_task.assert_called_once()
        assert response.status_code == 200
        data = response.json()
        assert data["url"] == url
        assert data["id"] == str(mock_article.id)
        assert data["title"] == mock_article.title
        assert data["description"] == mock_article.description
        assert data["imageUrl"] == mock_article.imageUrl


def test_delete_article(authorized_client, db_session, test_created_user, mock_pinecone):
    # Add a test article
    user_id = test_created_user["id"]

    article = Article(
        title=f"Test Article",
        url=f"http://test.com",
        imageUrl=f"http://test.com/",
        description=f"Test article",
        user_id=user_id)

    db_session.add(article)
    db_session.commit()

    with patch("knowledgenest.articles.router.delete_article_chunks_by_id") as mock_delete_chunks:
        response = authorized_client.delete(f"/articles/{article.id}")
        assert response.status_code == 204
        mock_delete_chunks.assert_called_once_with(
            article.id, mock_pinecone().Index())

    # Verify the article is deleted from the database
    deleted_article = db_session.query(Article).filter(
        Article.id == article.id).first()
    assert deleted_article is None

# Test service functions


def test_process_new_article(db_session, test_created_user):
    url = "http://example.com"
    user_id = test_created_user["id"]

    with patch("knowledgenest.articles.service.convert_properties_to_fields") as mock_extract:
        mock_extract.return_value = {
            "title": "Test Title", "description": "Test Description", "imageUrl": "http://example.com/image2.png", "url": url}

        article = process_new_article(url, user_id, db_session)
        mock_extract.assert_called_once()
        assert article.url == url
        assert article.user_id == user_id
        assert article.title == "Test Title"
        assert article.description == "Test Description"


def test_fetch_articles(db_session, test_created_user):
    user_id = test_created_user["id"]
    for i in range(5):
        article = Article(
            title=f"Test Article {i}", url=f"http://test{i}.com", user_id=user_id)
        db_session.add(article)
    db_session.commit()

    result = fetch_articles(user_id, db_session, offset=1, limit=2)
    assert result["articles_count"] == 5
    assert len(result["articles"]) == 2


def test_delete_article_by_id(db_session, test_created_user):
    user_id = test_created_user["id"]

    article = Article(
        title=f"Test Article",
        url=f"http://test.com",
        imageUrl=f"http://test.com/",
        description=f"Test article",
        user_id=user_id)
    db_session.add(article)
    db_session.commit()
    print(article.id)

    deleted_article = delete_article_by_id(
        article.id, user_id, db_session)
    assert deleted_article.id == article.id

    with pytest.raises(HTTPException):
        delete_article_by_id(article.id, user_id, db_session)

# Test utils functions


def test_extract_meta_properties():
    with patch("knowledgenest.articles.utils.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = """
        <html>
            <head>
                <meta property="og:title" content="Test Title">
                <meta property="og:description" content="Test Description">
                <meta name="description" content="Fallback Description">
            </head>
        </html>
        """
        mock_get.return_value = mock_response

        properties = extract_meta_properties("http://example.com")
        assert properties["title"] == "Test Title"
        assert properties["description"] == "Test Description"


def test_convert_properties_to_fields():
    properties = {
        "title": "Test Title",
        "description": "Test Description",
        "image": "http://example.com/image.jpg",
        "invalid_key": "This should be removed"
    }

    fields = convert_properties_to_fields(properties)
    assert "title" in fields
    assert "description" in fields
    assert "imageUrl" in fields
    assert "invalid_key" not in fields
    assert fields["imageUrl"] == properties["image"]
