# app/controllers.py

from app.config import (
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    oauth2_schema
    )
from datetime import (
    datetime, 
    timedelta
    )
from typing import Annotated
from fastapi import (
    Depends, 
    FastAPI, 
    HTTPException, 
    Security, 
    status,
    Header
    )
from fastapi.security import (
    OAuth2PasswordRequestForm,
    OAuth2PasswordBearer,
    SecurityScopes
    )
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.controllers.user_controller import get_user
from app.config import pwd_context
from app import schemas


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, session: Session):
    database_user = get_user(
        username=username, 
        session=session
        )
    
    if not verify_password(password, database_user.password):
        return f"Not match! {password}, {database_user.password}"

    return database_user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({
        "exp": expire
    })
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encode_jwt

def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_schema)], session: Session):
    if security_scopes:
        auth_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        auth_value = "Bearer"
    
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": auth_value
            },
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        token_scopes = payload.get("scopes", [])
        token_data = schemas.TokenData(
            scopes=token_scopes, 
            username=username
            )
    except (JWTError, ValidationError):
        raise credentials_exception
    
    user = get_user(username=token_data.username, session=session)

    if user is None:
        raise credentials_exception
    
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=401,
                detail="Not enough permissions",
                headers={
                    "WWW-Authenticate": auth_value
                    },
                )
    return user

def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session):
    database_user = authenticate_user(session=session, username=form_data.username, password=form_data.password)

    if not database_user:
        raise HTTPException(status_code=400, detail="Username or password incorrect.")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": database_user.username,
            "scopes": form_data.scopes
            },
        expires_delta=access_token_expires,
        )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

