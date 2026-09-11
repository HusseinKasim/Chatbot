from fastapi import APIRouter, Depends, HTTPException
from src.dependencies import get_current_user, get_db
from src import models
from sqlalchemy.orm import Session

router = APIRouter(prefix='/api/documents')

@router.get('/')
async def get_user_documents(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=401, detail='Invalid user')
    
    documents = db.query(models.Documents).filter(models.Documents.user_id == int(user['sub'])).all()
    return {'documents': documents}