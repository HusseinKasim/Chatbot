from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from hash import hash_password, verify_password
from dependencies import get_db, get_current_user, get_current_user_optional
import models
import pass_auth

router = APIRouter(prefix='/api/auth')

class RegisterData(BaseModel):
    firstName: str = Field(min_length=1)
    lastName: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)

class LoginData(BaseModel):
    email: str
    password: str

@router.get('/me') 
async def get_user_info(user=Depends(get_current_user_optional), db: Session = Depends(get_db)):
    if not user:
        return {'response': None, 'id': None, 'firstname': None, 'lastname': None }
    
    current_user = db.query(models.Users).filter(models.Users.id == int(user['sub'])).first()
    return {'response': 'success', 'id': int(user['sub']), 'firstname': current_user.first_name, 'lastname': current_user.last_name}


@router.post('/register') # Exception handling done
async def register(payload: RegisterData, db: Session = Depends(get_db)):

    existing_user = db.query(models.Users).filter(models.Users.email == payload.email.strip().lower()).first()
    if existing_user:
        raise HTTPException(status_code=409, detail='Email already exists!')

    # Encrypt password
    hashed_password = hash_password(payload.password)

    # Store data in database
    db_user = models.Users(first_name=payload.firstName.strip().capitalize(), last_name=payload.lastName.strip().capitalize(), email=payload.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user) 

    return {'response': "ok"}


@router.post('/login')
async def login(payload: LoginData, response: Response, db: Session = Depends(get_db)):
    # Verify password
    user = db.query(models.Users).filter(models.Users.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=401, detail='Invalid login credentials')
    
    if not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid login credentials')
    
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
    return {'response': 'authenticated'}


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