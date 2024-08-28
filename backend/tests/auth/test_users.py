from fastapi import status

def test_update_user_settings(authorized_client, test_created_user):
    new_settings = {"ai_provider": "openai"}
    response = authorized_client.put("/users/settings", json=new_settings)
    assert response.status_code == status.HTTP_200_OK
    updated_settings = response.json()
    assert updated_settings["ai_provider"] == "openai"

def test_update_user_settings_unauthorized(client):
    new_settings = {"ai_provider": "openai"}
    response = client.put("/users/settings", json=new_settings)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user(authorized_client, test_created_user):
    response = authorized_client.get("/users/me")
    assert response.status_code == status.HTTP_200_OK
    user_info = response.json()
    assert user_info["email"] == test_created_user["email"]
    assert user_info["setting"]["ai_provider"] == "mistral" # default provider

def test_get_current_user_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED