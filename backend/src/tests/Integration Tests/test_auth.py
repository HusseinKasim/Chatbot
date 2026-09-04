import pytest
from fastapi.testclient import TestClient
from fastapi import Response
from unittest.mock import Mock, patch
from src.app import app
from src.hash import hash_password, verify_password
from src.pass_auth import create_access_token, verify_access_token, create_refresh_token, verify_refresh_token
from http.cookies import SimpleCookie

client = TestClient(app)

# Test case: Test_User_Registration
def test_user_registration(sample_user):
    request = client.post('/api/auth/register', json={'firstName': sample_user['first_name'], 'lastName': sample_user['last_name'], 'email': sample_user['email'], 'password': sample_user['password']})

    # Assert successful response
    assert request.status_code == 200

    data = request.json()

    # Assert response exists
    assert data['response'] is not None

    # Assert response contains expected value
    assert data['response'] == 'ok'


# Test case: Test_User_Login
def test_user_login(sample_user):
    request = client.post('/api/auth/login', json={'email': sample_user['email'], 'password': sample_user['password']})

    # Assert successful response
    assert request.status_code == 200

    data = request.json()

    # Assert response exists
    assert data['response'] is not None

    # Assert response contains expected value
    assert data['response'] == 'authenticated'
