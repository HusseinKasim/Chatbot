from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from src.rag.ingest import ingest_doc
import shutil

router = APIRouter(prefix='/api/upload')

UPLOAD_DIR = Path('uploads')

@router.post('/')
async def upload(pdfFile: UploadFile = File(...)):
    # Create uploads folder (if not already created)
    UPLOAD_DIR.mkdir(exist_ok=True)
    # TODO: Add subdirectory for each user's documents
    
    # Save PDF
    file_path = UPLOAD_DIR / pdfFile.filename
    with open(file_path, 'wb') as result_file:
        shutil.copyfileobj(pdfFile.file, result_file)

    # Call ingest
    ingest_doc(file_path)

    return {'response': 'success'}