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
    HTTPException, 
    Security, 
    status,
    )
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.controllers.user_controller import get_user
from app.config import pwd_context, get_database
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

def get_current_user(
        token: str = Depends(oauth2_schema), 
        session: Session = Depends(get_database)
        ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
        )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    database_user = get_user(
        username=username, 
        session=session
        )
    
    if database_user is None:
        raise credentials_exception
    
    return database_user

def get_current_active_user(
        user: Annotated[schemas.UserSchema, Security(
            get_current_user, scopes=["me"]
            )]):
    return user

def get_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), 
        session: Session = Depends(get_database)
        ):
    database_user = authenticate_user(
        session=session, 
        username=form_data.username, 
        password=form_data.password
        )

    if not database_user:
        raise HTTPException(
            status_code=400, 
            detail="Username or password incorrect."
            )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": database_user.username},
        expires_delta=access_token_expires,
        )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def logout():
    """TODO: logout implementation. delete the token or session"""
    pass