from fastapi import Request, HTTPException
from database import Base, SessionLocal
import pass_auth

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_loggedin_user(request: Request):
    access_token = request.cookies.get('access_token')

    # Guest user
    if not access_token:
        raise HTTPException(status_code=401)  
     
    try:
        return pass_auth.verify_access_token(access_token)
    except:
        raise HTTPException(status_code=401)