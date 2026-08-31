import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.dependencies import get_db, get_current_user
from src import models

client = TestClient(app)

# Test case: Test_User_Chats_Fetch
def test_user_chats_fetch(db, db_user_auth, db_user_chat):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: db_user_auth

    response = client.get('/api/chats/')
    data = response.json()

    # Assert response exists
    assert data['chats'] is not None

    # Assert db chat is correctly fetched
    assert data['chats'][0]['id'] == db_user_chat.id
