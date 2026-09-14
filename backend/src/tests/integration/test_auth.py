from fastapi.testclient import TestClient
from src.app import app
from src import models
from src.dependencies import get_db
from src.hash import hash_password

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
def test_user_login(db, sample_user):
    app.dependency_overrides[get_db] = lambda: db

    sample_user_to_db = models.Users(first_name=sample_user['first_name'].strip().capitalize(), last_name=sample_user['last_name'].strip().capitalize(), email=sample_user['email'], password=hash_password(sample_user['password']))
    db.add(sample_user_to_db)
    db.commit()
    db.refresh(sample_user_to_db)

    request = client.post('/api/auth/login', json={'email': sample_user_to_db.email, 'password': sample_user['password']})

    # Assert successful response
    assert request.status_code == 200

    data = request.json()

    # Assert response exists
    assert data['response'] is not None

    # Assert response contains expected value
    assert data['response'] == 'authenticated'
