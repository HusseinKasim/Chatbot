from fastapi import Request, HTTPException
from langchain_openai import OpenAIEmbeddings
from .database import Base, SessionLocal
from . import pass_auth
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For cases that support logged-in users ONLY
def get_current_user(request: Request):
    access_token = request.cookies.get('access_token')

    # Guest user
    if not access_token:
        raise HTTPException(status_code=401)  
     
    try:
        return pass_auth.verify_access_token(access_token)
    except:
        raise HTTPException(status_code=401)
    

# For cases that support logged-in AND guest users
def get_current_user_optional(request: Request):
    access_token = request.cookies.get('access_token')

    # Guest user
    if not access_token:
        return None
     
    try:
        return pass_auth.verify_access_token(access_token)
    except:
        return None
    

def get_embeddings_model():
    # Create embedding model
    embeddings = OpenAIEmbeddings(
        model='text-embedding-3-small',
        api_key=OPENAI_API_KEY
    )
    
    return embeddings
    