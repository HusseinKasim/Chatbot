from fastapi import APIRouter, Depends, HTTPException
import models
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user, get_current_user_optional

router = APIRouter(prefix='/api/chats')
    
@router.get('/')  # Exception handling done
async def get_user_chats(user=Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return {'chats': []}
    
    chats = db.query(models.Chats).filter(models.Chats.user_id == int(user['sub'])).order_by(models.Chats.created_at.desc()).all()
    return {'chats': chats}


@router.get('/{chatID}/messages')  # Exception handling done
async def get_chat_messages(chatID: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    messages = db.query(models.Messages).filter(models.Messages.chat_id == chatID).all()
    return {'messages': messages}


@router.delete('/{chatID}') # Exception handling done
async def delete_chat(chatID: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Delete chat messages
    db.query(models.Messages).filter(models.Messages.chat_id == chatID).delete()

    # Delete chat
    chat = db.query(models.Chats).filter(models.Chats.id == chatID).first()
    if not chat:
        raise HTTPException(status_code=404, detail='Chat not found!')
    db.delete(chat)

    db.commit()
    return {'response': 'success'}
