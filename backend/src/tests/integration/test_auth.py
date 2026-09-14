from fastapi.testclient import TestClient
from src.app import app
from src import models
from src.dependencies import get_db

client = TestClient(app)

# Test case: Test_User_Registration
def test_user_registration(db, sample_user):
    app.dependency_overrides[get_db] = lambda: db

    request = client.post('/api/auth/register', json={'firstName': sample_user['first_name'], 'lastName': sample_user['last_name'], 'email': sample_user['email'], 'password': sample_user['password']})

    # Assert successful response
    assert request.status_code == 200

    data = request.json()
    
    registered_user = db.query(models.Users).filter(models.Users.email == sample_user['email'].strip().lower()).first()

    # Assert registered user exists
    assert registered_user is not None 

    # Assert response contains expected email value
    assert data['registered_user_email'] == registered_user.email.strip().lower()


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
