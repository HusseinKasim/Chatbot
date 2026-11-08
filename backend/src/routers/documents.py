from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_current_user, get_current_user_optional, get_db
from src import models
from sqlalchemy.orm import Session
import boto3
import os

router = APIRouter(prefix='/api/documents')

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
        