from fastapi.testclient import TestClient
from unittest.mock import patch
from src.app import app
from src.dependencies import get_db, get_current_user
from src import models
from src.rag.ingest import ingest_doc

client = TestClient(app)

# Test case: Test_Upload_Development_Environment
@patch('src.routers.upload.ingest_doc')
def test_upload_dev_environment(mock_ingest_doc, db, db_user_auth, sample_pdf_file, monkeypatch):
    monkeypatch.setenv('ENVIRONMENT', 'development')
    
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: db_user_auth

    try:
        mock_ingest_doc.return_value = {'document_id': 1, 'chunks': 5}
        response = client.post('/api/upload/', files={'pdfFile': sample_pdf_file})

        # Assert successful response
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()