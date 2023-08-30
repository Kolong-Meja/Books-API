# app/model.py

"""Model for Books table."""

from datetime import datetime
from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Date, 
    DateTime,
    ForeignKey,
    )
from sqlalchemy.orm import relationship
from app.config import Base


# create associate table for Books & Genres relationship.
class BookGenre(Base):
    __tablename__ = "BookGenres"

    book_id = Column("book_id", ForeignKey("Books.uuid"), primary_key=True)
    genre_id = Column("genre_id", ForeignKey("Genres.uuid"), primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow())

# create your model in here!
class Book(Base):
    __tablename__ = "Books"

    uuid = Column(String(36), primary_key=True)
    isbn = Column(String(13), nullable=True, unique=True)
    title = Column(String(255), unique=True, nullable=False)
    author_id = Column(String(36), ForeignKey("Authors.uuid"))
    pages = Column(Integer, nullable=False)
    publisher = Column(String(255), nullable=True)
    published = Column(Date, default=datetime(2017, 12, 4))
    timestamp = Column(DateTime, default=datetime.utcnow())

    # create relationship.
    author = relationship("Author", back_populates="books")
    genres = relationship("Genre", secondary="BookGenres", back_populates="books")

class Author(Base):
    __tablename__ = "Authors"

    uuid = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow())

    # create relationship.
    books = relationship("Book", back_populates="author")

class Genre(Base):
    __tablename__ = "Genres"

    uuid = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow())

    # create relationship.
    books = relationship("Book", secondary="BookGenres", back_populates="genres")
    