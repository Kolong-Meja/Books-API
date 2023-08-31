# app/controllers/user_controller.py

"""CRUD Logic for User"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import (
    models, 
    schemas
    )
from app.config import pwd_context

# hash the password first.
def password_hash(password: str):
    return pwd_context.hash(password)

def get_all_users(session: Session, skip: int = 0, limit: int = 100):
    return session.query(models.User).offset(skip).limit(limit).all()

def create_user(user: schemas.UserSchemaCreate, session: Session):
    database_user = models.User(
        uuid=user._uuid,
        username=user.username,
        password=password_hash(user.password),
        timestamp=user.timestamp
    )
    session.add(database_user)
    session.commit()
    session.refresh(database_user)
    session.close()
    return database_user

def get_user(username: str, session: Session):
    if not session.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=404, detail=f"User '{username}' not found.")

    return session.query(models.User).filter(models.User.username == username).first()

def update_user(username: str, user: schemas.UserSchemaUpdate, session: Session):
    database_user = session.query(models.User).filter(models.User.username == username).first()

    if not database_user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found.")

    new_username = user.username
    hash_password = password_hash(user.password)

    database_user.username = new_username
    database_user.password = hash_password

    session.commit()
    session.refresh(database_user)
    session.close()
    return database_user

def delete_user(username: str, session: Session):
    database_user = session.query(models.User).filter(models.User.username == username).first()

    if not database_user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found.")
    
    session.delete(database_user)
    session.commit()
    session.close()
    return {
        "message": "User deleted successfully!"
    }

