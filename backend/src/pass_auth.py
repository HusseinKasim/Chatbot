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
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = 'HS256'
TOKEN_EXPIRATION_TIME_HOURS = 1

# Create JWT Token
def create_token(user_id: int):
    payload = {
        'sub': str(user_id),
        'exp': datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRATION_TIME_HOURS) 
    }

    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify JWT Token
def verify_token(token: str):
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    return payload