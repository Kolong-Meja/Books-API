# app/controllers/authentication_controller.py

from app.config import (
    pwd_context,
    SECRET_KEY, 
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
    )
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.controllers.user_controller import get_user
from app import models
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from fastapi import Depends, HTTPException

"""CRUD Logic for Authentication"""

def verify_password(plain_password: str, hash_password: str):
    return pwd_context.verify(plain_password, hash_password)

def authenticate_user(username: str, password: str, session: Session):
    database_user = get_user(
        username=username, 
        session=session
        )
    if not verify_password(password, models.User.password):
        raise Exception("password not match.")
    
    return database_user

def create_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()

    if not expire_delta:
        expire = datetime.utcnow() + timedelta(minutes=15)
    else:
        expire = datetime.utcnow() + expire_delta
    
    to_encode.update({"expire_time": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def login(session: Session, form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    if not authenticate_user(
        username=username, 
        password=password, 
        session=session
        ):
        raise HTTPException(status_code=400, detail="Username or Password incorrect.")
    else:
        access_token = create_token(
            data={
                "sub": username
                }, 
            expire_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        return {
            "access_token": {access_token},
            "token_type": "bearer"
        }
