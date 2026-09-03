import pytest
from fastapi.testclient import TestClient
from src.app import app
from src.dependencies import get_db, get_current_user_optional, get_current_user
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


# Test case: Test_User_Chat_Messages_Fetch
def test_user_chat_messages_fetch(db, db_user_auth, db_user_chat, db_user_chat_messages):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: db_user_auth

    response = client.get(f'/api/chats/{db_user_chat.id}/messages')
    data = response.json()

    # Assert successful response
    assert response.status_code == 200 

    # Assert response exists
    assert data['messages'] is not None

    # Assert db user message is correctly fetched
    if data['messages'][0]['role'] == 'user':
        user_message_id = data['messages'][0]['id']
    assert user_message_id == db_user_chat_messages[0].id

    # Assert db assistant message is correctly fetched
    if data['messages'][1]['role'] == 'assistant':
        assistant_message_id = data['messages'][1]['id']
    assert assistant_message_id == db_user_chat_messages[1].id


# Test case: Test_User_Chat_Delete
def test_user_chat_delete(db, db_user_auth, db_user_chat):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: db_user_auth

    response = client.delete(f'/api/chats/{db_user_chat.id}/')

    # Assert successful response
    assert response.status_code == 200

    deleted_db_chat = db.query(models.Chats).filter(models.Chats.id == db_user_chat.id, models.Chats.user_id == db_user_auth['sub']).first()

    # Assert deleted db chat does not exist anymore
    assert deleted_db_chat is None