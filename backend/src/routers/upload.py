from fastapi import APIRouter, UploadFile, File, Depends
from pathlib import Path
from src.rag.ingest import ingest_doc
import shutil
from sqlalchemy.orm import Session
from src.dependencies import get_db, get_current_user
import boto3
from dotenv import load_dotenv
import os
import uuid

router = APIRouter(prefix='/api/upload')

load_dotenv()

ENVIRONMENT = os.getenv('ENVIRONMENT')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY') 
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY') 
AWS_REGION = os.getenv('AWS_REGION') 
AWS_BUCKET = os.getenv('AWS_BUCKET') 

@router.post('/')
async def upload(pdfFile: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Create uploads folder (if not already created)
    UPLOAD_DIR = Path('uploads') / user['sub']
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Save PDF
    file_path = UPLOAD_DIR / pdfFile.filename
    with open(file_path, 'wb') as result_file:
        shutil.copyfileobj(pdfFile.file, result_file)

    s3_key = None

    if ENVIRONMENT == 'production':
        # Push to AWS S3
        try: 
            pdfFile.file.seek(0)

            s3_client = boto3.client('s3', aws_access_key=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
            s3_key = f"users/{user['sub']}/documents/{pdfFile.filename}--{uuid.uuid4()}"

            s3_client.upload_fileobj(pdfFile.file, AWS_BUCKET, s3_key)
        except Exception as e:
            print(f'S3 upload failed: {e}')
            raise
            
    # Call ingest
    results = ingest_doc(file_path, db, user, s3_key=s3_key)

    return {'response': 'success', 'document_added': results['document_id'], 'chunks_added': results['chunks']}