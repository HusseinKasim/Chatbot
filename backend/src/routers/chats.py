from fastapi import APIRouter, Depends, Request, HTTPException
import models
from database import Base, SessionLocal
from sqlalchemy.orm import Session
import pass_auth

router = APIRouter(prefix='/api/chats')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request):
    token = request.cookies.get('access_token')

    # Guest user
    if not token:
        return None  
     
    try:
        return pass_auth.verify_token(token)
    except:
        return None
    
@router.get('/')
async def get_user_chats(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(models.Users).filter(models.Users.id == int(user['sub'])).first():
        chats = db.query(models.Chats).filter(models.Chats.user_id == int(user['sub'])).order_by(models.Chats.created_at.desc()).all()
        return {'chats': chats}
    else:
        print('error') # Handle user not found
    return {'chats': None}


@router.get('/{chatID}/messages')
async def get_chat_messages(chatID: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(models.Users).filter(models.Users.id == int(user['sub'])).first():
        messages = db.query(models.Messages).filter(models.Messages.chat_id == chatID).all()
        return {'messages': messages}
    else:
        print('error') # Handle user not found
    return {'messages': None}


@router.delete('/{chatID}') 
async def delete_chat(chatID: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if db.query(models.Users).filter(models.Users.id == int(user['sub'])).first():
        # Delete chat messages
        db.query(models.Messages).filter(models.Messages.chat_id == chatID).delete()
        db.commit()

        # Delete chat
        chat = db.query(models.Chats).filter(models.Chats.id == chatID).first()
        db.delete(chat)
        db.commit()
        return {'response': 'success'}
    else:
        return {'response': 'invalid'}