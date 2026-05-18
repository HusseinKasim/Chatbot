import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from typing import List
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from hash import encrypt_password, verify_password
import auth

app = FastAPI()
 
load_dotenv()

models.Base.metadata.create_all(bind=engine)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# Pydantic classes
class Message(BaseModel):
    role: str
    content: str

class ChatMessages(BaseModel):
    messages: List[Message]

class RegisterData(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str


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
        return auth.verify_token(token)
    except:
        return None


# HTTP POST endpoint
@app.post('/api/process-prompt')
async def captureUserInput(chatMessages: ChatMessages, user = Depends(get_current_user), db: Session = Depends(get_db)):
    if user:
        user_id = user['sub']
    else:
        user_id = 0 # Handle guest user better
    print(user_id) # Current user's ID

    chat_completion = client.chat.completions.create(
        messages=
        [
            {
                'role': msg.role,  
                'content': msg.content,
            }   
            for msg in chatMessages.messages
        ], 
        model='llama-3.3-70b-versatile',
    )
    chatbot_response = chat_completion.choices[0].message.content
    return {'response': chatbot_response}


@app.post('/api/register')
async def register(payload: RegisterData, db: Session = Depends(get_db)):
    if payload.firstName != '' and payload.lastName != '' and payload.email != '' and payload.password  != '':
        # Encrypt password
        encrypted_password = encrypt_password(payload.password)

        # Store data in database
        db_user = models.Users(first_name=payload.firstName.capitalize(), last_name=payload.lastName.capitalize(), email=payload.email, password=encrypted_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user) 
        return {'response': "ok"}
    # Handle Exception: Empty input field/-s


@app.post('/api/login')
async def login(payload: LoginData, response: Response, db: Session = Depends(get_db)):
    # Verify password
    user = db.query(models.Users).filter(models.Users.email == payload.email).first()
    if not user:
        # Handle exception: Email does not exist
        return {'response', 'invalid'}
    
    password_verification = verify_password(payload.password, user.password)
    if password_verification:
        token = auth.create_token(user.id)
        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,
            secure=False,
            samesite='lax'
        )
        return {'response': 'authentificated'}
    
    # Handle exception: Password not verified
    return {'response', 'invalid'}


@app.post('/api/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    # Handle Exception: cookie does not exist/already deleted
    return {'response': 'logged out'}


@app.get('/api/me')
async def get_user_info(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return {'response': None, 'id': None, 'firstname': None, 'lastname': None }
    
    current_user = db.query(models.Users).filter(models.Users.id == user['sub']).first()
    return {'response': 'success', 'id': user['sub'], 'firstname': current_user.first_name, 'lastname': current_user.last_name}