import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from typing import List

app = FastAPI()
 
load_dotenv()

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


# HTTP POST endpoint
@app.post("/api/process-prompt")
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
        model='llama-3.3-70b-versatile',
    )
    chatbot_response = chat_completion.choices[0].message.content
    return {"response": chatbot_response}
