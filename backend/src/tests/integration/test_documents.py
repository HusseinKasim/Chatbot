from fastapi.testclient import TestClient
from src.app import app
from src.dependencies import get_db, get_current_user, get_current_user_optional
from unittest.mock import patch
from src import models
from src.rag.ingest import ingest_doc

client = TestClient(app)


# Test case: Test_User_Documents_Fetch
def test_user_documents_fetch(db, db_user_auth, db_user_document):
    try:
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
    finally:
        app.dependency_overrides.clear()


# Test case: Test_User_Documents_Fetch_Empty
def test_user_documents_fetch_empty(db, db_user_auth):
    try:
        app.dependency_overrides[get_db] = lambda: db
        app.dependency_overrides[get_current_user_optional] = lambda: db_user_auth

        response = client.get('/api/documents/')
        data = response.json()

        # Assert successful response
        assert response.status_code == 200 

        # Assert response is empty
        assert data['documents'] == []
    finally:
        app.dependency_overrides.clear()

 
# Test case: Test_User_Documents_Fetch_Invalid_User
def test_user_documents_fetch_invalid_user(db): 
    try:
        app.dependency_overrides[get_db] = lambda: db
        app.dependency_overrides[get_current_user_optional] = lambda: None

        response = client.get('/api/documents/')

        # Assert unauthorized response
        assert response.status_code == 401 

        data = response.json()
        
        # Assert response contains the expected error message
        assert data['detail'] == 'Invalid user'
    finally:
        app.dependency_overrides.clear()


# Test case: Test_Upload_Dev_Environment
@patch('src.routers.upload.ingest_doc')
def test_upload_dev_environment(mock_ingest_doc, db, db_user_auth, sample_pdf_file, monkeypatch):
    try:
        monkeypatch.setenv('ENVIRONMENT', 'development')
            
        app.dependency_overrides[get_db] = lambda: db
        app.dependency_overrides[get_current_user] = lambda: db_user_auth
        
        mock_ingest_doc.return_value = {'document_id': 1, 'chunks': 5}
        response = client.post('/api/upload/', files={'pdfFile': sample_pdf_file})

        # Assert successful response
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


# Test case: Test_Ingest_Doc_Dev_Environment
def test_ingest_doc_dev_environment(db, db_user_auth, sample_pdf_file_path):
    try:
        app.dependency_overrides[get_db] = lambda: db
        app.dependency_overrides[get_current_user] = lambda: db_user_auth

        results = ingest_doc(sample_pdf_file_path, db, db_user_auth, s3_key=None)

        # Assert document added to db
        new_db_document = db.query(models.Documents).filter(models.Documents.user_id == db_user_auth['sub']).order_by(models.Documents.id.desc()).first()
        assert new_db_document is not None
        assert results['document_id'] == new_db_document.id

        # Assert document chunks added to db
        new_db_document_chunks = db.query(models.Chunks).join(models.Documents).filter(models.Documents.user_id == db_user_auth['sub'], models.Chunks.document_id == new_db_document.id).all()
        assert results['chunks'] == len(new_db_document_chunks)
    finally:
        app.dependency_overrides.clear()


# Test case: Test_Upload_Unsupported_File_Type
@patch('src.routers.upload.ingest_doc')
def test_upload_unsupported_file_type(mock_ingest_doc, db, db_user_auth, sample_exe_file, monkeypatch):
    try:
        monkeypatch.setenv('ENVIRONMENT', 'development')
                
        app.dependency_overrides[get_db] = lambda: db
        app.dependency_overrides[get_current_user] = lambda: db_user_auth
            
        mock_ingest_doc.return_value = {'document_id': 1, 'chunks': 5}
        response = client.post('/api/upload/', files={'pdfFile': sample_exe_file})
    
        # Assert unsupported media type response
        assert response.status_code == 415

        data = response.json()

        # Assert response contains the expected error message
        assert data['detail'] == 'File type is not supported. Uploaded file must be a PDF.'
    
        # Assert mocked function is not called
        mock_ingest_doc.assert_not_called()
    finally:
        app.dependency_overrides.clear()