from fastapi import APIRouter, Depends, HTTPException
from groq import Groq
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from src import models
from src.dependencies import get_db, get_current_user
import os
from src.rag import retrieval

router = APIRouter(prefix='/api/prompt')
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
GROQ_MODEL = 'openai/gpt-oss-120b'

# Pydantic classes
class LoggedInUserPromptData(BaseModel):
    prompt: str
    chatID: int

class Message(BaseModel):
    role: str
    content: str

class ChatMessages(BaseModel):
    messages: List[Message]

# Guest prompt endpoint
@router.post('/guest')
async def captureUserInput(chatMessages: ChatMessages):
    # Raise exception if empty prompt
    for msg in chatMessages.messages:
        if msg.role == 'user' and msg.content == '':
            raise HTTPException(status_code=400, detail='Prompt cannot be empty')
        
    try:
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
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail='Groq LLM request failed')

    chatbot_response = chat_completion.choices[0].message.content
    return {'response': chatbot_response}


# User prompt endpoint
@router.post('/user')   
async def captureUserInput(promptData: LoggedInUserPromptData, user = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return {'chatID': 0, 'response': 'invalid'}
        
    if promptData.chatID == 0:
    # Add row in chats db, assign chatID, and return chatID
        new_chat = models.Chats(chat_title=promptData.prompt, user_id=int(user['sub']))
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        promptData.chatID = new_chat.id

    # Retrieve roles and chat messages from messages db (via chatID) of authorized user
    messages_query = (db.query(models.Messages).join(models.Chats, models.Messages.chat_id == models.Chats.id).filter(models.Chats.user_id == int(user['sub']), models.Messages.chat_id == promptData.chatID).order_by(models.Messages.created_at.asc()).all())   

    # Add row in messages db to add user's first prompt
    new_message = models.Messages(role='user', message_text=promptData.prompt, chat_id=promptData.chatID)
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    
    llm_messages = [
                {
                    'role': msg.role,  
                    'content': msg.message_text,
                }   
                for msg in messages_query
            ]

    try:
        # Add RAG context to prompt and llm_messages
        updated_prompt = await retrieval.context_retrieval(prompt=promptData.prompt, db=db, user=int(user['sub']))
    except Exception as e:
        print(f"RAG failed: {e}")
        updated_prompt = None

    if not updated_prompt:
        updated_prompt = promptData.prompt

    llm_messages.append({'role': 'user', 'content': updated_prompt})

    try:
        # Pass information into model
        chat_completion = client.chat.completions.create(
            messages=llm_messages,
            model=GROQ_MODEL,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail='Groq LLM request failed')
        
    chatbot_response = chat_completion.choices[0].message.content 

    # Add row of bot response into messages db
    new_bot_message = models.Messages(role='assistant', message_text=chatbot_response, chat_id=promptData.chatID)
    db.add(new_bot_message)
    db.commit()
    db.refresh(new_bot_message)

    return {'chatID': promptData.chatID, 'response': chatbot_response}




