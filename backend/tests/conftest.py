import pytest
import os
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from knowledgenest.database import Base, get_db

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def mock_pinecone():
    with patch("knowledgenest.vector_database.Pinecone") as mock_pinecone:
        mock_index = Mock()
        mock_pinecone.return_value.Index.return_value = mock_index
        mock_pinecone.return_value.list_indexes.return_value = []
        mock_pinecone.return_value.describe_index.return_value.status = {"ready": True}
        yield mock_pinecone

@pytest.fixture(scope="function")
def vector_db(mock_pinecone):
    from knowledgenest.vector_database import get_vector_db
    return get_vector_db()

@pytest.fixture(scope="function")
def client(db_session):
    from knowledgenest.app import app
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]

@pytest.fixture
def test_user():
    return {"email": "test@example.com", "password": "testpassword"}

def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before returning the exit status to the system.
    """
    os.remove("./test.db")

