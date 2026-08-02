from fastapi import APIRouter, UploadFile
from pathlib import Path
import shutil

router = APIRouter(prefix='/api/upload')

UPLOAD_DIR = Path('uploads')

@router.post('/')
async def upload(pdfFile: UploadFile):
    # Save PDF
    file_path = UPLOAD_DIR / pdfFile.filename
    with open(file_path, 'wb') as result_file:
        shutil.copyfileobj(pdfFile.file, result_file)

    # Call ingest

    return {'response': 'success'}