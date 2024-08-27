from knowledgenest.auth.service import create_access_token
from tests.conftest import test_user, client


def test_signup(test_user, client):
    response = client.post("/auth/signup", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]


def test_login(test_user, client):
    # First, create a user
    client.post("/auth/signup", json=test_user)

    # Now try to login
    response = client.post(
        "/auth/login", data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["email"] == test_user["email"]


def test_verify_token(client):
    token = create_access_token(data={"username": "test@example.com"})
    response = client.post("/auth/verify", json={"token": token})
    assert response.status_code == 200


def test_verify_invalid_token(client):
    response = client.post("/auth/verify", json={"token": "not.valid.token"})
    assert response.status_code == 404
