# app/controller/book_genre_controller.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import (
    models, 
    schemas
    )


"""
Make sure all of this CRUD logic are used in route.
"""
def get_all_book_genres(session: Session, skip: int = 0, limit: int = 100):
    return session.query(models.BookGenre).offset(skip).limit(limit).all()

def create_book_genres(book_genre: schemas.BookGenreSchema, session: Session):
    database_book = session.query(models.Book).filter(models.Book.uuid == book_genre.book_id).first()
    database_genre = session.query(models.Genre).filter(models.Genre.uuid == book_genre.genre_id).first()
    database_book_genre = models.BookGenre(
        book_id=database_book.uuid,
        genre_id=database_genre.uuid
        )
    
    session.add(database_book_genre)
    session.commit()
    session.refresh(database_book_genre)
    session.close()
    return database_book_genre

def get_book_data(book_id: str, session: Session):
    if not session.query(models.Book).join(models.BookGenre, models.BookGenre.book_id == book_id).order_by(models.BookGenre.timestamp.asc()).first():
        raise HTTPException(status_code=404, detail=f"'{book_id}' not found.")
    
    return session.query(models.Book).join(models.BookGenre, models.BookGenre.book_id == book_id).order_by(models.BookGenre.timestamp.asc()).first()
    
def get_genre_data(genre_id: str, session: Session):
    if not session.query(models.Genre).join(models.BookGenre, models.BookGenre.genre_id == genre_id).order_by(models.BookGenre.timestamp.asc()).first():
        raise HTTPException(status_code=404, detail=f"'{genre_id}' not found.")

    return session.query(models.Genre).join(models.BookGenre, models.BookGenre.genre_id == genre_id).order_by(models.BookGenre.timestamp.asc()).first()
