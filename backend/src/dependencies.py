from fastapi import Request, HTTPException
from database import Base, SessionLocal
import pass_auth

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