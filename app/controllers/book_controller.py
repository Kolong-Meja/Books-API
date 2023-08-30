# app/controllers/book.py

"""CRUD Logic for Book"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import (
    models, 
    schemas
    )


"""
Make sure all of this CRUD logic are used in route.
"""
def get_book(title: str, session: Session):
    if not session.query(models.Book).filter(models.Book.title == title).first():
        raise HTTPException(status_code=404, detail=f"'{title}' not found.")
    
    return session.query(models.Book).filter(models.Book.title == title).first()

def get_all_books(session: Session, skip: int = 0, limit: int = 100):
    return session.query(models.Book).offset(skip).limit(limit).all()

def create_book(author_id: str, book: schemas.BookSchemaCreate, session: Session):
    database_book = models.Book(
        uuid=book._uuid,
        title=book.title,
        pages=book.pages,
        published=book.published,
        timestamp=book.timestamp,
        author_id=author_id
        )
    session.add(database_book)
    session.commit()
    session.refresh(database_book)
    session.close()
    return database_book

def update_book(title: str, book: schemas.BookSchemaUpdate, session: Session):
    database_book = session.query(models.Book).filter(models.Book.title == title).first()
    
    if not database_book:
        raise HTTPException(status_code=404, detail=f"'{title}' not found.")
    
    book_data = book.model_dump(exclude_unset=True)

    for key, value in book_data.items():
        setattr(database_book, key, value)
    
    session.commit()
    session.refresh(database_book)
    session.close()
    return database_book

def delete_book(title: str, session: Session):
    database_book = session.query(models.Book).filter(models.Book.title == title).first()

    if not database_book:
        raise HTTPException(status_code=404, detail=f"'{title}' not found.")
    
    session.delete(database_book)
    session.commit()
    session.close()
    return {
        "message": f"'{title}' book deleted successfully!"
    }

def update_author_by_title(title: str, book: schemas.BookAuthorSchemaUpdate, session: Session):
    database_book = session.query(models.Book).filter(models.Book.title == title).first()
    
    if not database_book:
        raise HTTPException(status_code=404, detail=f"'{title}' not found.")
    
    data = book.model_dump(exclude_unset=False)

    for key, value in data.items():
        setattr(database_book, key, value)
    
    session.commit()
    session.refresh(database_book)
    session.close()
    return database_book

