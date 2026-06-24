
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src import models
from src.database import Base, engine, SessionLocal
from src.routers import prompt, auth, chats

app = FastAPI()

load_dotenv()

models.Base.metadata.create_all(bind=engine)

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
