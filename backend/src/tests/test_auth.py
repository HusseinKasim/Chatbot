import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from src.app import app
from src.hash import hash_password, verify_password

client = TestClient(app)

# Test case: Test_User_Registration
def test_user_registration(sample_user, db):
    request = client.post('/api/auth/register', json={'payload': sample_user, 'db': db})
    assert request.status_code == 200
    
    data = request.json()
    assert data['response'] is not None
    assert data['response'] == 'ok'


# Test case: Test_Password_Hashing
def test_password_hashing(sample_user):
    test_password = sample_user['password']

    hashed_password = hash_password(test_password)

    assert isinstance(hashed_password, str)
    assert hashed_password != test_password


# Test case: Test_Password_Verification
def test_password_verification(sample_user):
    test_password = sample_user['password']

    hashed_password = hash_password(test_password)
    
    assert verify_password(test_password, hashed_password)