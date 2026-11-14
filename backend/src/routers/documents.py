from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from src.dependencies import get_current_user, get_current_user_optional, get_db
from src import models
from src.rag.ingest import ingest_doc
from sqlalchemy.orm import Session
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import os
import shutil
import uuid

router = APIRouter(prefix='/api/documents')

load_dotenv()

AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
AWS_BUCKET = os.getenv('AWS_BUCKET')
ENVIRONMENT = os.getenv('ENVIRONMENT')


@router.get('/')
async def get_user_documents(user=Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail='Invalid user')
    
    documents = db.query(models.Documents).filter(models.Documents.user_id == int(user['sub'])).all()
    return {'documents': documents}


@router.post('/upload')
async def upload(pdfFile: UploadFile = File(...), db: Session = Depends(get_db), user = Depends(get_current_user)):
    # Check if file type is supported (pdf)
    if pdfFile.content_type != 'application/pdf': # add other types as required
        raise HTTPException(status_code=415, detail='File type is not supported. Uploaded file must be a PDF.')

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

            s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
            s3_key = f"users/{user['sub']}/documents/{pdfFile.filename}--{uuid.uuid4()}"

            s3_client.upload_fileobj(pdfFile.file, AWS_BUCKET, s3_key)
        except ClientError as e:
            print(f'S3 document upload failed: {e}')
            raise
            
    # Call ingest
    results = ingest_doc(file_path, db, user, s3_key=s3_key)

    return {'response': 'success', 'document_added': results['document_id'], 'chunks_added': results['chunks']}


@router.get('/load/{documentID}')
async def load_user_document_(documentID: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    expiration = 3000

    document = db.query(models.Documents).join(models.Users, models.Documents.user_id == models.Users.id).filter(models.Users.id == user['sub'], models.Documents.id == documentID).first()
    key = document.s3_key
    if ENVIRONMENT == 'production':
        presigned_url = s3_client.generate_presigned_url('get_object',
                                            Params={
                                                'Bucket': AWS_BUCKET,
                                                'Key': key,            
                                                'ResponseContentType': 'application/pdf',
                                                'ResponseContentDisposition': 'inline' 
                                            },
                                            ExpiresIn=expiration)
            
        return {'response': 'AWS S3 document successfully retrieved!', 'documentID': documentID, 'documentTitle': str(document.document_name), 's3_url': presigned_url}
    else:
        raise HTTPException(status_code=403, detail= 'Invalid envrionment! Must be on production to use this feature.')


@router.delete('/delete/{documentID}')
def delete_user_document(documentID: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Get document from DB
    document = db.query(models.Documents).filter(models.Documents.id == documentID, models.Documents.user_id == user['sub']).first()
    if not document:
        raise HTTPException(status_code=404, detail='Document not found!')

    # Delete document chunks
    db.query(models.Chunks).filter(models.Chunks.document_id == document.id).delete()
    
    # Delete document
    db.query(models.Documents).filter(models.Documents.id == document.id).delete()
    db.commit()
        
    # Delete document from uploads folder
    UPLOAD_DIR = Path('uploads') / user['sub']
    local_document = document.document_name + '.pdf'
    file_path = UPLOAD_DIR / local_document
    if file_path.exists():
        os.remove(Path(file_path))

    # Delete document from AWS
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION)
    key = document.s3_key
    if ENVIRONMENT == 'production':
        try:
            s3_client.delete_object(
                Bucket = AWS_BUCKET,
                Key = key
            )
        except ClientError as e:
            print(f'S3 document deletion failed: {e}')
            raise
