from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
from src.rag.ingest import ingest_doc
import shutil
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_current_user

router = APIRouter(prefix='/api/upload')

@router.post('/')
async def upload(pdfFile: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    
    # Create uploads folder (if not already created)
    UPLOAD_DIR = Path('uploads') / user['sub']
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Save PDF
    file_path = UPLOAD_DIR / pdfFile.filename
    with open(file_path, 'wb') as result_file:
        shutil.copyfileobj(pdfFile.file, result_file)

    # Call ingest
    results = ingest_doc(file_path, db, user)

    return {'response': 'success', 'document_added': results['document_id'], 'chunks_added': results['chunks']}