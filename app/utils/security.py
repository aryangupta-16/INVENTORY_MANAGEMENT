from datetime import datetime, timedelta
from jose import JWTError # @unresolvedImport
import jwt # @unresolvedImport
from dotenv import load_dotenv
import os
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session # @UnresolvedImport
from fastapi import Depends, HTTPException, status
from app.config.database import get_db
from app.repository.User_repo import get_user_by_email

load_dotenv()

SECRET_KEY = "123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

bearerScheme =  HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token:str):
    return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

def get_current_user(credential: HTTPAuthorizationCredentials = Depends(bearerScheme), db: Session = Depends(get_db)):
    token = credential.credentials
    print("Token received:", token)
    try:
        payload = decode_access_token(token)
        print("Decoded payload:", payload)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication Token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication Token")
    
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user