from fastapi.testclient import TestClient
from unittest.mock import patch
from src.app import app
from src.dependencies import get_db, get_current_user
from src import models
from src.rag.ingest import ingest_doc

client = TestClient(app)

# Test case: Test_Upload_Dev_Environment
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


# Test case: Test_Ingest_Doc_Dev_Env
def test_ingest_doc_dev_environment(db, db_user_auth, sample_pdf_file_path):
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: db_user_auth

    try:
        results = ingest_doc(sample_pdf_file_path, db, db_user_auth, s3_key=None)

        # Assert document added to db
        new_db_document = db.query(models.Documents).filter(models.Documents.user_id == db_user_auth['sub']).order_by(models.Documents.id.desc).first()
        assert results['document_added'] == new_db_document.id

        # Assert document chunks added to db
        new_db_document_chunks = db.query(models.Chunks).join(models.Documents).filter(models.Documents.user_id == db_user_auth['sub'], models.Chunks.document_id == new_db_document.id).all()
        assert results['chunks'] == len(new_db_document_chunks)
    finally:
        app.dependency_overrides.clear()