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


# Test case: Test_Access_Token_Creation
def test_access_token_creation():
    USER_ID = 616 

    access_token = create_access_token(USER_ID)

    # Assert access token exists
    assert access_token is not None


# Test case: Test_Access_Token_Verification
def test_access_token_verification():
    USER_ID = 616 
    
    access_token = create_access_token(USER_ID)
    payload = verify_access_token(access_token)

    # Assert payload exists
    assert payload is not None

    # Assert access token's userID matches the correct userID value
    assert payload['sub'] == str(USER_ID)


# Test case: Test_Refresh_Token_Creation
def test_refresh_token_creation():
    USER_ID = 616 

    refresh_token = create_refresh_token(USER_ID)

    # Assert refresh token exists
    assert refresh_token is not None


# Test case: Test_Refresh_Token_Verification
def test_refresh_token_verification():
    USER_ID = 616 
    
    refresh_token = create_refresh_token(USER_ID)
    payload = verify_refresh_token(refresh_token)

    # Assert payload exists
    assert payload is not None

    # Assert refresh token's userID matches the correct userID value
    assert payload['sub'] == str(USER_ID)


# Test case: Test_Password_Hashing
def test_password_hashing(sample_user):
    test_password = sample_user['password']

    hashed_password = hash_password(test_password)

    # Assert hashed password is of string data type
    assert isinstance(hashed_password, str)

    # Assert hashed password contains a different value than the user's password
    assert hashed_password != test_password


# Test case: Test_Password_Verification
def test_password_verification(sample_user):
    test_password = sample_user['password']

    hashed_password = hash_password(test_password)

    # Assert user's password can be correctly verified to hashed password
    assert verify_password(test_password, hashed_password)


# Test case: Test_Access_Token_Cookie_Security
def test_access_token_cookie_security():
    USER_ID = 616 
    response = Response()

    access_token = create_access_token(USER_ID)
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=True,
        samesite='none'
    )
    cookie_header = response.headers.get('set-cookie')

    # Assert cookie header exists
    assert cookie_header is not None

    cookie = SimpleCookie()
    cookie.load(cookie_header)
    cookie_data = cookie['access_token']

    # Assert cookie is configured with the HttpOnly attribute
    assert cookie_data['httponly'] is True

    # Assert cookie is configured with the Secure attribute
    assert cookie_data['secure'] is True

    # Assert cookie is configured with SameSite=None
    assert cookie_data['samesite'].lower() == 'none'


# Test case: Test_Refresh_Token_Cookie_Security
def test_refresh_token_cookie_security():
    USER_ID = 616 
    response = Response()

    refresh_token = create_refresh_token(USER_ID)
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='none'
    )
    cookie_header = response.headers.get('set-cookie')

    # Assert cookie header exists
    assert cookie_header is not None

    cookie = SimpleCookie()
    cookie.load(cookie_header)
    cookie_data = cookie['refresh_token']

    # Assert cookie is configured with the HttpOnly attribute
    assert cookie_data['httponly'] is True

    # Assert cookie is configured with the Secure attribute
    assert cookie_data['secure'] is True

    # Assert cookie is configured with SameSite=None
    assert cookie_data['samesite'].lower() == 'none'
    
