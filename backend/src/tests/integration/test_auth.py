from fastapi.testclient import TestClient
from src.app import app
from src import models
from src.dependencies import get_db
from src.hash import hash_password
from src.pass_auth import create_access_token, create_refresh_token

client = TestClient(app)

# Test case: Test_User_Registration
def test_user_registration(db, sample_user):
    app.dependency_overrides[get_db] = lambda: db

    response = client.post('/api/auth/register', json={'firstName': sample_user['first_name'], 'lastName': sample_user['last_name'], 'email': sample_user['email'], 'password': sample_user['password']})

    # Assert successful response
    assert response.status_code == 200

    data = response.json()

    registered_user = db.query(models.Users).filter(models.Users.email == sample_user['email'].strip().lower()).first()

    # Assert registered user exists
    assert registered_user is not None 

    # Assert response contains expected email value
    assert data['registered_user_email'] == registered_user.email.strip().lower()


# Test case: Test_User_Registration_Duplicate_Email
def test_user_registration_duplicate_email(db, sample_user):
    app.dependency_overrides[get_db] = lambda: db
    sample_user_2 = {
        'first_name': 'Sample2', 
        'last_name': 'User2', 
        'email': 'sampleuser@gmail.com', # Duplicate email as sample_user
        'password': 'testpassword2'
    }

    # Add sample_user_2 to DB
    sample_user_2 = models.Users(first_name=sample_user_2['first_name'].strip().capitalize(), last_name=sample_user_2['last_name'].strip().capitalize(), email=sample_user_2['email'], password=sample_user_2['password'])
    db.add(sample_user_2)
    db.commit()

    # Register sample_user with the same email
    response = client.post('/api/auth/register', json={'firstName': sample_user['first_name'], 'lastName': sample_user['last_name'], 'email': sample_user['email'], 'password': sample_user['password']})

    # Assert conflict error
    assert response.status_code == 409

    data = response.json()

    # Assert correct error message
    assert data['detail'] == 'Email already exists!'

    email_count = db.query(models.Users).filter(models.Users.email == sample_user['email']).count()
    
    # Assert the duplicate was not added
    assert email_count == 1


# Test case: Test_User_Login
def test_user_login(db, sample_user):
    app.dependency_overrides[get_db] = lambda: db

    sample_user_to_db = models.Users(first_name=sample_user['first_name'].strip().capitalize(), last_name=sample_user['last_name'].strip().capitalize(), email=sample_user['email'], password=hash_password(sample_user['password']))
    db.add(sample_user_to_db)
    db.commit()
    db.refresh(sample_user_to_db)

    response = client.post('/api/auth/login', json={'email': sample_user_to_db.email, 'password': sample_user['password']})

    # Assert successful response
    assert response.status_code == 200

    data = response.json()

    # Assert response exists
    assert data['response'] is not None

    # Assert JWT cookies exist
    assert client.cookies.get('access_token') is not None
    assert client.cookies.get('refresh_token') is not None


# Test case: Test_User_Login_Non_Existent_Email
def test_user_login_non_existent_email(db, sample_user):
    app.dependency_overrides[get_db] = lambda: db

    # Set up non-existent email
    NON_EXISTENT_EMAIL = 'nonexistentemail@gmail.com'

    # Add sample user to db
    sample_user_to_db = models.Users(first_name=sample_user['first_name'].strip().capitalize(), last_name=sample_user['last_name'].strip().capitalize(), email=sample_user['email'], password=hash_password(sample_user['password']))
    db.add(sample_user_to_db)
    db.commit()
    db.refresh(sample_user_to_db)

    response = client.post('/api/auth/login', json={'email': NON_EXISTENT_EMAIL, 'password': sample_user['password']})

    # Assert unauthorized response
    assert response.status_code == 401

    data = response.json()

    # Assert response contains the expected error message
    assert data['detail'] == 'Invalid login credentials'


# Test case: Test_User_Login_Invalid_Password
def test_user_login_invalid_password(db, sample_user):
    app.dependency_overrides[get_db] = lambda: db

    # Set up invalid password
    INVALID_PASSWORD = 'invalidpassword'

    # Add sample user to db
    sample_user_to_db = models.Users(first_name=sample_user['first_name'].strip().capitalize(), last_name=sample_user['last_name'].strip().capitalize(), email=sample_user['email'], password=hash_password(sample_user['password']))
    db.add(sample_user_to_db)
    db.commit()
    db.refresh(sample_user_to_db)

    response = client.post('/api/auth/login', json={'email': sample_user['email'], 'password': INVALID_PASSWORD})

    # Assert unauthorized response
    assert response.status_code == 401

    data = response.json()

    # Assert response contains the expected error message
    assert data['detail'] == 'Invalid login credentials'


# Test case: Test_User_Logout
def test_user_logout():
    USER_ID = 616

    # Create JWT tokens
    access_token = create_access_token(USER_ID)
    refresh_token = create_refresh_token(USER_ID)

    # Create cookies with JWT tokens
    client.cookies.set('access_token', access_token)
    client.cookies.set('refresh_token', refresh_token)

    response = client.post('/api/auth/logout')

    # Assert successful response
    assert response.status_code == 200

    data = response.json()

    # Assert response exists
    assert data['response'] is not None

    set_cookie_headers = response.headers.get_list('set-cookie')

    # Assert JWT cookies were deleted
    assert any('access_token=' in cookie and 'Max-Age=0' in cookie for cookie in set_cookie_headers)
    assert any('refresh_token=' in cookie and 'Max-Age=0' in cookie for cookie in set_cookie_headers)