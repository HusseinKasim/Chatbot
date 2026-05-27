from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from hash import encrypt_password, verify_password
from dependencies import get_db, get_current_loggedin_user
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

@router.get('/me')
async def get_user_info(user=Depends(get_current_loggedin_user), db: Session = Depends(get_db)):
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
        access_token = pass_auth.create_access_token(user.id)
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='lax'
        )

        refresh_token = pass_auth.create_refresh_token(user.id)
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
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
    response.delete_cookie('refresh_token')
    # Handle Exception: cookie does not exist/already deleted
    return {'response': 'logged out'}


@router.post('/refresh')
async def create_new_access_token(request: Request, response:Response):
    # Verify refresh token
    refresh_token = request.cookies.get('refresh_token')
    if not refresh_token:
        return {'response': None}
    
    payload = pass_auth.verify_refresh_token(refresh_token)

    # Create access token in cookie
    access_token = pass_auth.create_access_token(payload['sub'])
    response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='lax'
        )
    return {'response': 'success'}