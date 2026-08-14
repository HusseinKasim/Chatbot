import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from src.app import app
from conftest import test_user

client = TestClient(app)

# Test case: Guest_User_Prompt_Response
@patch('src.routers.prompt.client.chat.completions.create')
def test_guest_user_prompt_response(mock_groq):
    test_messages = [{
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
