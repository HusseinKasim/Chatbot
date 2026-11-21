
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import prompt, auth, chats, documents

app = FastAPI()

load_dotenv()

try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Connection to the DB port failed. Is the DB up?")
    exit(1)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "http://localhost:5173",
        "https://chatbot-r1ui.onrender.com"], # Render Frontend
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

app.include_router(prompt.router)
app.include_router(auth.router)
app.include_router(chats.router)
app.include_router(documents.router)