from fastapi import APIRouter, Depends, HTTPException, Response, Request
from groq import Groq
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import models
import pass_auth
import os

router = APIRouter(prefix='/api/prompt')
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = 'llama-3.3-70b-versatile'

# Pydantic classes
class LoggedInUserPromptData(BaseModel):
    prompt: str
    chatID: int

class Message(BaseModel):
    role: str
    content: str

class ChatMessages(BaseModel):
    messages: List[Message]

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

# Guest prompt endpoint
@router.post('/guest')
async def captureUserInput(chatMessages: ChatMessages):
    chat_completion = client.chat.completions.create(
        messages=
        [
            {
                'role': msg.role,  
                'content': msg.content,
            }   
            for msg in chatMessages.messages
        ], 
        model=GROQ_MODEL,
    ) # Handle exception for no response
    chatbot_response = chat_completion.choices[0].message.content
    return {'response': chatbot_response}


# User prompt endpoint
@router.post('/user')
async def captureUserInput(promptData: LoggedInUserPromptData, user = Depends(get_current_user), db: Session = Depends(get_db)):
    # Verify user token is valid (by comparing with db)
    if db.query(models.Users).filter(models.Users.id == int(user['sub'])).first():

        if promptData.chatID == 0:
        # Add row in chats db, assign chatID, and return chatID
            new_chat = models.Chats(chat_title=promptData.prompt[0:25], user_id=int(user['sub']))
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            promptData.chatID = new_chat.id

        # Add row in messages db to add user's first prompt
        new_message = models.Messages(role='user', message_text=promptData.prompt, chat_id=promptData.chatID)
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        # Retrieve roles and chat messages from messages db (via chatID) of authorized user
        messages_query = (db.query(models.Messages).join(models.Chats, models.Messages.chat_id == models.Chats.id).filter(models.Chats.user_id == int(user['sub']), models.Messages.chat_id == promptData.chatID).order_by(models.Messages.created_at.asc()).all())   
        
        # Pass information into model
        chat_completion = client.chat.completions.create(
            messages=
            [
                {
                    'role': msg.role,  
                    'content': msg.message_text,
                }   
                for msg in messages_query
            ], 
            model=GROQ_MODEL,
        ) # Handle exception for no response
        chatbot_response = chat_completion.choices[0].message.content 

        # Add row of bot response into messages db
        new_bot_message = models.Messages(role='assistant', message_text=chatbot_response, chat_id=promptData.chatID)
        db.add(new_bot_message)
        db.commit()
        db.refresh(new_bot_message)

        return {'chatID': promptData.chatID, 'response': chatbot_response}
    
    return {'chatID': 0, 'response': 'invalid'}


