# app/schemas.py

"""Schemas for Books tables."""

from uuid import uuid4 as uuid_val
from datetime import (
    date, 
    datetime
    )
from pydantic import (
    BaseModel, 
    Field, 
    PrivateAttr, 
    ConfigDict
    )
from typing import List


"""
The purpose of schemas is to make documentation easiest to read for users.
"""
class BookBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    _uuid: str = PrivateAttr(
        default_factory=lambda: uuid_val().hex,
        )
    isbn: str = Field(
        title="ISBN", 
        description="ISBN of the book.",
        max_length=13
        )
    title: str = Field(
        title="Title",
        description="Title of the book.",
        max_length=255,
        )
    pages: int = Field(
        title="Pages",
        description="Number of book pages.",
        )
    publisher: str = Field(
        title="Publisher",
        description="Publisher of the book.",
        max_length=255
    )
    published: date = Field(
        default=datetime.now().strftime("%Y-%m-%d"),
        title="Published",
        description="Book publication date."
        )
    timestamp: datetime = Field(
        default=datetime.utcnow(),
        title="Timestamp",
        description="Datetime of book data changes.",
        )

class BookSchemaCreate(BookBase):
    pass

class BookSchemaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    isbn: str | None = Field(
        default=None,
        title="ISBN", 
        description="ISBN of the book.",
        max_length=13
        )
    title: str | None = Field(
        default=None,
        title="Title",
        description="Title of the book.",
        max_length=255,
        )
    pages: int | None = Field(
        default=None,
        title="Pages",
        description="Number of book pages.",
        )
    publisher: str | None = Field(
        default=None,
        title="Publisher",
        description="Publisher of the book.",
        max_length=255
    )
    published: date = Field(
        default=datetime.now().strftime("%Y-%m-%d"),
        title="Published",
        description="Book publication date."
        )
    _timestamp: datetime | None = PrivateAttr(
        default_factory=datetime.utcnow
        )

class BookAuthorSchemaUpdate(BaseModel):
    author_id: str

class AuthorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    _uuid: str = PrivateAttr(
        default_factory=lambda: uuid_val().hex,
        )
    name: str = Field(
        title="Name",
        description="Name of the author.",
        max_length=255
        )
    timestamp: datetime = Field(
        default=datetime.now(),
        title="Timestamp",
        description="Datetime of author data changes.",
        )

class AuthorSchemaCreate(AuthorBase):
    pass

class AuthorSchemaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = Field(
        default=None,
        title="Name",
        description="Name of the author.",
        max_length=255
        )
    _timestamp: datetime | None = PrivateAttr(
        default_factory=datetime.utcnow
    )

class GenreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    _uuid: str = PrivateAttr(
        default_factory=lambda: uuid_val().hex,
        )
    name: str = Field(
        title="Name",
        description="Name of the genre.",
        max_length=255
        )
    timestamp: datetime = Field(
        default=datetime.utcnow(),
        title="Timestamp",
        description="Datetime of genre data changes.",
        )

class GenreSchemaCreate(GenreBase):
    pass

class GenreSchemaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str | None = Field(
        default=None,
        title="Name",
        description="Name of the genre.",
        max_length=255
        )
    _timestamp: datetime = PrivateAttr(
        default_factory=datetime.utcnow
        )

class BookGenreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    book_id: str = Field(
        title="Book ID", 
        description="Book identifiers."
        )
    genre_id: str = Field(
        title="Genre ID",
        description="Genre identifiers."
        )
    timestamp: datetime = Field(
        default=datetime.utcnow(),
        title="Timestamp",
        description="Datetime of book genre data changes."
        )

class BookSchema(BookBase):
    author: AuthorBase
    genres: List[GenreBase]

class BookAuthorSchema(BookBase):
    author: AuthorBase

class AuthorSchema(AuthorBase):
    books: List[BookBase]

class GenreSchema(GenreBase):
    books: List[BookBase]

class BookGenreSchema(BookGenreBase):
    pass

class DeleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str = Field(
        default="Data deleted successfully!"
        )

