import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends
from fastapi.security import HTTPBearer
from dotenv import load_dotenv

# Optional authentification
security = HTTPBearer(auto_error=False)

# Constants
load_dotenv()
ACCESS_TOKEN_SECRET_KEY = os.getenv('JWT_ACCESS_TOKEN_SECRET_KEY')
REFRESH_TOKEN_SECRET_KEY = os.getenv('JWT_REFRESH_TOKEN_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRATION_TIME_HOURS = 1
REFRESH_TOKEN_EXPIRATION_TIME_HOURS = 72

# Create JWT access token
def create_access_token(user_id: int):
    payload = {
        'sub': str(user_id),
        'type': 'access',
        'exp': datetime.now(timezone.utc) + timedelta(hours=ACCESS_TOKEN_EXPIRATION_TIME_HOURS) 
    }

    token = jwt.encode(payload=payload, key=ACCESS_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify JWT access token
def verify_access_token(token: str):
    payload = jwt.decode(jwt=token, key=ACCESS_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
    return payload

# Create JWT refresh token
def create_refresh_token(user_id: int):
    payload = {
        'sub': str(user_id),
        'type': 'refresh',
        'exp': datetime.now(timezone.utc) + timedelta(hours=REFRESH_TOKEN_EXPIRATION_TIME_HOURS) 
    }
    
    token = jwt.encode(payload=payload, key=REFRESH_TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify JWT refresh token
def verify_refresh_token(token: str):
    payload = jwt.decode(jwt=token, key=REFRESH_TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
    return payload