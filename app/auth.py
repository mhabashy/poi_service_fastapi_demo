from fastapi import Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from .database import get_db
from .models import APIKey
from jose import jwt, JWTError
from datetime import datetime, timedelta
import secrets
import string
import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "development_secret_key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

def generate_api_key(length=32):
    """Generate a random API key."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_jwt_token(data: dict):
    """Create a new JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_jwt_token(token: str):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def verify_api_key(
    api_key: str = Security(API_KEY_HEADER),
    db: Session = Depends(get_db)
):
    """Verify the API key from header is valid."""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key header is missing",
        )
    
    db_api_key = db.query(APIKey).filter(APIKey.key == api_key, APIKey.is_active == True).first()
    
    if not db_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API Key",
        )
    
    return db_api_key