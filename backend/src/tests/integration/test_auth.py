from fastapi.testclient import TestClient
from src.app import app

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
