# app/controller/book_genre_controller.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app import (
    models, 
    schemas
    )
from app.controllers.authentication_controller import get_current_user


"""
Make sure all of this CRUD logic are used in route.
"""
def get_all_book_genres(
        session: Session, 
        skip: int = 0, 
        limit: int = 100,
        auth: schemas.UserSchema = Depends(get_current_user),
        ):
    data = session.query(models.BookGenre).offset(skip).limit(limit).all()
    if auth: return data

def create_book_genres(
        book_genre: schemas.BookGenreSchema, 
        session: Session,
        auth: schemas.UserSchema = Depends(get_current_user)
        ):
    if auth:
        database_book = session.query(models.Book).filter(models.Book.uuid == book_genre.book_id).first()
        database_genre = session.query(models.Genre).filter(models.Genre.uuid == book_genre.genre_id).first()
        database_book_genre = models.BookGenre(
            uuid=book_genre._uuid,
            book_id=database_book.uuid,
            genre_id=database_genre.uuid
            )

        session.add(database_book_genre)
        session.commit()
        session.refresh(database_book_genre)
        session.close()
        return database_book_genre

def update_book_genre(
        book_genre_id: str,
        book_genre: schemas.BookGenreSchema,
        session: Session,
        auth: schemas.UserSchema = Depends(get_current_user)
        ):
    if auth:
        database_book_genre = session.query(models.BookGenre).filter(models.BookGenre.uuid == book_genre_id).first()

        if not data:
            raise HTTPException(status_code=404, detail=f"Book Genre with ID '{book_genre_id}' not found.")

        data = book_genre.model_dump(exclude_unset=False)

        for key, value in data.items():
            setattr(database_book_genre, key, value)

        session.commit()
        session.refresh(database_book_genre)
        session.close()
        return data

def delete_book_genre(
        book_genre_id: str,
        session: Session,
        auth: schemas.UserSchema = Depends(get_current_user)
        ):
    if auth:
        data = session.query(models.BookGenre).filter(models.BookGenre.uuid == book_genre_id).first()

        if not data:
            raise HTTPException(status_code=404, detail=f"Book Genre with id '{book_genre_id}' not found.")
        
        session.delete(data)
        session.commit()
        session.close()
        return {
            "message": "BookGenre deleted successfully!"
        }

