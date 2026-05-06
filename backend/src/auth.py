import os
import jwt
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import HTTPBearer
from dotenv import load_dotenv

# Optional authentification
security = HTTPBearer(auto_error=False)

# Constants
load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET_KEY')
ALGORITHM = ''

# Create JWT Token
def create_token():
    # IMPLEMENT
    return 

# Verify JWT Token
def verify_token():
    # IMPLEMENT
    return