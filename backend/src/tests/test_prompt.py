import pytest
from fastapi.TestClient import TestClient
from app import app

client = TestClient(app)

def test_guest():
    test_messages = [{
        'role': 'user'
        'content': 'Hi! How are you?'
    },
    {
        'role': 'assistant'
        'content': 'I am fine. How about you?'
    },
    {
        'role': 'user'
        'content': 'I am fine. What is the definition of the world test?'
    }]

    response = client.post('/api/prompt/guest', json={test_messages}) # Must not use the real Groq API
    assert response.status_code = 200

