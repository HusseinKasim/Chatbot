
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import models
from database import Base, engine, SessionLocal
import pass_auth
from routers import prompt, auth, chats

app = FastAPI()

load_dotenv()

models.Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

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

app.include_router(prompt.router)
app.include_router(auth.router)
app.include_router(chats.router)
