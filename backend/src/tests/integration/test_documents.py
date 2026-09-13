from fastapi.testclient import TestClient
from src.app import app
from src.dependencies import get_db, get_current_user_optional
from src import models

client = TestClient(app)

# Test case: Test_User_Documents_Fetch
def test_user_documents_fetch(db, db_user_auth, db_user_document):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user_optional] = lambda: db_user_auth

    response = client.get('/api/documents/')
    data = response.json()

    # Assert successful response
    assert response.status_code == 200 

    # Assert response exists
    assert data['documents'] is not None

    # Assert db document is correctly fetched
    assert data['documents'][0]['id'] == db_user_document.id


# Test case: test_user_documents_fetch_empty
def test_user_documents_fetch_empty(db, db_user_auth):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user_optional] = lambda: db_user_auth

    response = client.get('/api/documents/')
    data = response.json()

    # Assert successful response
    assert response.status_code == 200 

    # Assert response is empty
    assert data['documents'] == []

 
# Test case: Test_User_Documents_Fetch_Invalid_User
def test_user_documents_fetch_invalid_user(db):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user_optional] = lambda: None

    response = client.get('/api/documents/')

    # Assert successful response
    assert response.status_code == 401 

    data = response.json()
    
    # Assert db document is correctly fetched
    assert data['detail'] == 'Invalid user'
