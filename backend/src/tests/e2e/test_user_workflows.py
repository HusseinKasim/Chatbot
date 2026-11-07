from fastapi import HTTPException
from fastapi.testclient import TestClient
from src.app import app
from src import models

client = TestClient(app, base_url='https://testserver')

# Test case: Test_Successful_User_Workflow_No_Doc
def test_successful_user_workflow_no_doc(sample_user, db):
    first_prompt = 'Hello. What is the weather like today?'
    second_prompt = 'What about tomorrow?'
    chatID = 0 # New chat

    # Register new user successfully
    response = client.post('/api/auth/register', json={'firstName': sample_user['first_name'], 'lastName': sample_user['last_name'], 'email': sample_user['email'], 'password': sample_user['password']})
    assert response.status_code == 200

    data = response.json()
    assert data['registered_user_email'] == sample_user['email']

    # Log into user successfully
    response = client.post('/api/auth/login', json={'email': sample_user['email'], 'password': sample_user['password']})
    assert response.status_code == 200

    data = response.json()
    assert data['response'] == 'authenticated'

    # Submit prompt successfully
    response = client.post('/api/prompt/user', json={'prompt': first_prompt, 'chatID': chatID})
    assert response.status_code == 200

    data = response.json()
    llm_response = data['response']
    new_chat_id = data['chatID']

    assert new_chat_id != 0
    assert llm_response is not None

    # Submit second prompt successfully (same chat)
    response = client.post('/api/prompt/user', json={'prompt': second_prompt, 'chatID': new_chat_id})
    assert response.status_code == 200

    data = response.json()
    llm_response = data['response']

    assert llm_response is not None
    assert data['chatID'] == new_chat_id

    # Check if both user messages both bot responses exist in the db for this new chat ID
    messages = db.query(models.Messages).filter(models.Messages.chat_id == new_chat_id).all()

    user_messages = [m for m in messages if m.role == 'user']
    assert len(user_messages) == 2 # Verify both user queries exist

    assistant_messages = [m for m in messages if m.role == 'assistant']
    assert len(assistant_messages) == 2 # Verify both bot responses exist

    # Log out
    response = client.post('/api/auth/logout')
    assert response.status_code == 200
