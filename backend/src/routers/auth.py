from fastapi import APIRouter, Depends, HTTPException, Response, Request
from database import Base, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from hash import encrypt_password, verify_password
import models
import pass_auth

router = APIRouter(prefix='/api/auth')

class RegisterData(BaseModel):
    firstName: str
    lastName: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

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

@router.get('/me')
async def get_user_info(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return {'response': None, 'id': None, 'firstname': None, 'lastname': None }
    
    current_user = db.query(models.Users).filter(models.Users.id == int(user['sub'])).first()
    return {'response': 'success', 'id': int(user['sub']), 'firstname': current_user.first_name, 'lastname': current_user.last_name}


@router.post('/register')
async def register(payload: RegisterData, db: Session = Depends(get_db)):
    if payload.firstName != '' and payload.lastName != '' and payload.email != '' and payload.password  != '':
        # Encrypt password
        encrypted_password = encrypt_password(payload.password)

        # Store data in database
        db_user = models.Users(first_name=payload.firstName.capitalize(), last_name=payload.lastName.capitalize(), email=payload.email, password=encrypted_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user) 
        return {'response': "ok"}
    # Handle Exception: Empty input field/-s


@router.post('/login')
async def login(payload: LoginData, response: Response, db: Session = Depends(get_db)):
    # Verify password
    user = db.query(models.Users).filter(models.Users.email == payload.email).first()
    if not user:
        # Handle exception: Email does not exist
        return {'response': 'invalid'}
    
    password_verification = verify_password(payload.password, user.password)
    if password_verification:
        token = pass_auth.create_token(user.id)
        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,
            secure=False,
            samesite='lax'
        )
        return {'response': 'authentificated'}
    
    # Handle exception: Password not verified
    return {'response': 'invalid'}


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    # Handle Exception: cookie does not exist/already deleted
    return {'response': 'logged out'}

