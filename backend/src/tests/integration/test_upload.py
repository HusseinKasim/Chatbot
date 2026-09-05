from fastapi.testclient import TestClient
from unittest.mock import patch
from src.app import app
from src.dependencies import get_db, get_current_user
from src import models
from pytest import MonkeyPatch

client = TestClient(app)

# Test case: Test_Upload_Development_Environment
def test_upload_dev_environment(db, db_user_auth, sample_pdf_file):
    app.dependency_override[get_db] = lambda: db
    app.dependency_override[get_current_user] = lambda: db_user_auth

    monkeypatch = MonkeyPatch()
    monkeypatch.setenv('ENVIRONMENT', 'development')

    response = client.post('/api/upload/', file={'pdfFile': sample_pdf_file})

    # Assert successful response
    assert response.status_code == 200

    data = response.json()
    
    # Assert document added to db
    new_db_document = db.query(models.Documents).filter(models.Documents.user_id == db_user_auth['sub']).order_by(models.Documents.id.desc).first()
    assert data['document_added'] == new_db_document.id

    # Assert document chunks added to db
    new_db_document_chunks = db.query(models.Chunks).join(models.Documents).filter(models.Documents.user_id == db_user_auth['sub'], models.Chunks.document_id == new_db_document.id).all()
    assert data['chunks'] == len(new_db_document_chunks)