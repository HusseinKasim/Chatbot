import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.dependencies import get_db, get_current_user_optional
from src import models

client = TestClient(app)

# Test case: Test_User_Chats_Fetch
def test_user_chats_fetch(db, db_user_auth, db_user_chat):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user_optional] = lambda: db_user_auth

    response = client.get('/api/chats/')
    data = response.json()

    # Assert successful response
    assert response.status_code == 200 

    # Assert response exists
    assert data['chats'] is not None

    # Assert db chat is correctly fetched
    assert data['chats'][0]['id'] == db_user_chat.id


# Test case: Test_User_Chats_Fetch_Invalid_User
def test_user_chats_fetch_invalid_user(db):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user_optional] = lambda: None

    response = client.get('/api/chats/')
    data = response.json()

    # Assert unauthorized response
    assert response.status_code == 401 

    # Assert response contains the expected error message 
    assert data['detail'] == 'Invalid user'