from fastapi.testclient import TestClient
from src.app import app
from src.dependencies import get_db, get_current_user
from src import models

client = TestClient(app)

# Test case: Test_User_Documents_Fetch
def test_user_documents_fetch(db, db_user_auth, db_user_document):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: db_user_auth

    response = client.get('/api/documents/')
    data = response.json()

    # Assert successful response
    assert response.status_code == 200 

    # Assert response exists
    assert data['documents'] is not None

    # Assert db document is correctly fetched
    assert data['documents'][0]['id'] == db_user_document.id
