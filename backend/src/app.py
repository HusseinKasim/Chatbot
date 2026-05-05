import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from typing import List
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from hash import encrypt_password

app = FastAPI()
 
load_dotenv()

models.Base.metadata.create_all(bind=engine)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# HTTP POST endpoint
@app.post("/api/process-prompt")
async def captureUserInput(chatMessages: ChatMessages, db: Session = Depends(get_db)):
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


@app.post("/api/register")
async def register(payload: RegisterData, db: Session = Depends(get_db)):
    # Encrypted password
    encrypted_password = encrypt_password(payload.password)

    db_user = models.Users(first_name=payload.firstName, last_name=payload.lastName, email=payload.email, password=encrypted_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 
    return {'response': "ok"}