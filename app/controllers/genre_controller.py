# app/controllers/genre_controller.py

"""CRUD Logic for Genre"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import (
    models, 
    schemas
    )


"""
Make sure all of this CRUD logic are used in route.
"""
def get_genre(name: str, session: Session):
    if not session.query(models.Genre).filter(models.Genre.name == name).first():
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")
    
    return session.query(models.Genre).filter(models.Genre.name == name).first()

def get_genres(session: Session, skip: int = 0, limit: int = 100):
    return session.query(models.Genre).offset(skip).limit(limit).all()

def create_genre(genre: schemas.GenreSchemaCreate, session: Session):
    database_genre = models.Genre(
        uuid=genre._uuid,
        name=genre.name,
        description=genre.description,
        timestamp=genre.timestamp
    )

    session.add(database_genre)
    session.commit()
    session.refresh(database_genre)
    session.close()
    return database_genre

def update_genre(name: str, genre: schemas.GenreSchemaUpdate, session: Session):
    database_genre = session.query(models.Genre).filter(models.Genre.name == name).first()

    if not database_genre:
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")
    
    genre_data = genre.model_dump(exclude_unset=True)

    for key, value in genre_data.items():
        setattr(database_genre, key, value)

    session.commit()
    session.refresh(database_genre)
    session.close()
    return database_genre

def delete_genre(name: str, session: Session):
    database_genre = session.query(models.Genre).filter(models.Genre.name == name).first()

    if not database_genre:
        raise HTTPException(status_code=404, detail=f"'{name}' not found.")

    session.delete(database_genre)
    session.commit()
    session.close()
    return {
        "message": "Genre deleted successfully!"
    }
