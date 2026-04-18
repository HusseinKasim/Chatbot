import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

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

# Pydantic class
class UserPrompt(BaseModel):
    prompt: str

# HTTP POST endpoint
@app.post("/api/process-prompt")
async def captureUserInput(prompt: UserPrompt):
    print(prompt)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': prompt.prompt
            }
        ], 
        model='llama-3.3-70b-versatile',
    )
    chatbot_response = chat_completion.choices[0].message.content
    print(chatbot_response)
    return {"response": chatbot_response}
