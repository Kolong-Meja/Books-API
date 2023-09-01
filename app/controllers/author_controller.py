# app/controllers/author.py

"""CRUD Logic for Author"""

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from app import (
    models, 
    schemas
    )

"""
Make sure all of this CRUD logic are used in route.
"""
def get_author(name: str, session: Session):
    if not session.query(models.Author).filter(models.Author.name == name).first():
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")
    
    return session.query(models.Author).filter(models.Author.name == name).first()

def get_all_authors(session: Session, skip: int = 0, limit: int = 100):
    return session.query(models.Author).options(joinedload(models.Author.books)).offset(skip).limit(limit).all()

def create_author(author: schemas.AuthorSchemaCreate, session: Session):
    database_author = models.Author(
        uuid=author._uuid,
        name=author.name,
        timestamp=author.timestamp
        )
    session.add(database_author)
    session.commit()
    session.refresh(database_author)
    return database_author

def update_author(name: str, author: schemas.AuthorSchemaUpdate, session: Session):
    database_author = session.query(models.Author).filter(models.Author.name == name).first()

    if not database_author:
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")

    author_data = author.model_dump(exclude_unset=True)

    for key, value in author_data.items():
        setattr(database_author, key, value)
    
    session.commit()
    session.refresh(database_author)
    session.close()
    return database_author

def delete_author(name: str, session: Session):
    database_author = session.query(models.Author).filter(models.Author.name == name).first()

    if not database_author:
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")

    session.delete(database_author)
    session.commit()
    return {
        "message": f"Author '{name}' data deleted successfully!"
    }



