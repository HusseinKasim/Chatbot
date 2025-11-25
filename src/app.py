from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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
@app.post("/capture_prompt")
async def captureUserInput(prompt: UserPrompt):
    print(prompt)
    return prompt
