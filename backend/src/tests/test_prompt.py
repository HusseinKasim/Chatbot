import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from src.app import app
from src.dependencies import get_db, get_current_user
from src.pass_auth import create_access_token, verify_access_token

client = TestClient(app)

# Test case: Test_Guest_User_Prompt_Response
@patch('src.routers.prompt.client.chat.completions.create')
def test_guest_user_prompt_response(mock_groq):
    test_messages = [{
         'role': 'assistant',
        'content': 'Hello! How can I help you today?'
    },
    {
        'role': 'user',
        'content': 'Hi! How are you?'
    },
    {
        'role': 'assistant',
        'content': 'I am fine. How about you?'
    },
    {
        'role': 'user',
        'content': 'I am fine. What is the definition of the word test?'
    }]

    mock_groq.return_value.choices[0].message.content = 'A test is a planned procedure or set of actions executed to evaluate whether a software application, hardware component, or system functions correctly, securely, and efficiently.'
    response = client.post('/api/prompt/guest', json={'messages': test_messages})
    assert response.status_code == 200
    
    data = response.json()
    assert data['response'] is not None
    assert data['response'] == mock_groq.return_value.choices[0].message.content


# Test case: Test_Guest_User_Prompt_Empty
@patch('src.routers.prompt.client.chat.completions.create')
def test_guest_user_prompt_empty(mock_groq):
    test_messages = [{
            'role': 'assistant',
            'content': 'Hello! How can I help you today?'
            },
            {
            'role': 'user',
            'content': ''
        }]

    mock_groq.return_value.choices[0].message.content = "I've processed an empty prompt!"
    response = client.post('/api/prompt/guest', json={'messages': test_messages})
    assert response.status_code == 400

    data = response.json()
    assert data['detail'] == 'Prompt cannot be empty'


# Test case: Test_Logged_In_User_Prompt_Response
@patch('src.routers.prompt.client.chat.completions.create')
def test_logged_in_user_prompt_response(mock_groq, db, db_user):

    prompt = 'What is a test?'
    chatID = 0

    app.dependency_overrides[get_db] = lambda: db

    access_token = create_access_token(db_user.id)
    payload = verify_access_token(access_token)

    app.dependency_overrides[get_current_user] = lambda: payload

    mock_groq.return_value.choices[0].message.content = 'A test is a planned procedure or set of actions executed to evaluate whether a software application, hardware component, or system functions correctly, securely, and efficiently.'
    response = client.post('/api/prompt/user', json={'prompt': prompt, 'chatID': chatID})

    print(response.json())

    assert response.status_code == 200
    
    data = response.json()
    assert data['response'] is not None
    assert data['response'] == mock_groq.return_value.choices[0].message.content

    app.dependency_overrides.clear()