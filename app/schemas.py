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
    ConfigDict,
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
    synopsis: str = Field(
        title="Synopsis",
        description="Synopsis of the book"
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
    synopsis: str | None = Field(
        default=None,
        title="Synopsis",
        description="Synopsis of the book"
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
    author_id: str = Field(
        title="UUID", 
        description="""Identifier of authors data | **NOTE**: Check first \
        the UUID of authors to make changes."""
        )

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
    birth_date: date = Field(
        default=date(year=1970, month=1, day=1),
        title="Birthdate",
        description="Birthdate of author."
        )
    nationality: str = Field(
        title="Nationality",
        description="Nationality of the author.",
        max_length=255
        )
    biography: str = Field(
        title="Biography",
        description="Biography of the author."
        )
    timestamp: datetime = Field(
        default=datetime.now(),
        title="Timestamp",
        description="Datetime of author data changes.",
        )

# for displaying UUID of authors data
class AuthorSchema(AuthorBase):
    uuid: str = Field(
        default_factory=lambda: uuid_val().hex,
        title="UUID",
        description="Identifier for authors data."
        )
    name: str = Field(
        title="Name",
        description="Name of the author.",
        max_length=255
        )
    birth_date: date = Field(
        default=date(year=1970, month=1, day=1),
        title="Birthdate",
        description="Birthdate of author."
        )
    nationality: str = Field(
        title="Nationality",
        description="Nationality of the author.",
        max_length=255
        )
    biography: str = Field(
        title="Biography",
        description="Biography of the author."
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
    birth_date: date | None = Field(
        default=date(year=1970, month=1, day=1),
        title="Birthdate",
        description="Birthdate of author."
        )
    nationality: str | None = Field(
        default=None,
        title="Nationality",
        description="Nationality of the author.",
        max_length=255
        )
    biography: str | None = Field(
        default=None,
        title="Biography",
        description="Biography of the author."
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
    description: str = Field(
        title="Description",
        description="Description of the genre."
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
    description: str | None = Field(
        default=None,
        title="Description",
        description="Description of the genre."
        )
    _timestamp: datetime = PrivateAttr(
        default_factory=datetime.utcnow
        )

class BookGenreBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    _uuid: str = PrivateAttr(
        default_factory=lambda: uuid_val().hex
        )
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

class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    _uuid: str = PrivateAttr(
        default_factory=lambda: uuid_val().hex
    )
    username: str = Field(
        title="Username",
        description="Name of user that will be used for authentication.",
        max_length=255
        )
    password: str = Field(
        title="Password",
        description="Password of user that used for authentication.",
        max_length=255
        )
    description: str | None = Field(
        default=None, 
        title="Description", 
        description="Description of the user"
        )
    timestamp: datetime = Field(
        default=datetime.utcnow(),
        title="Timestamp",
        description="Datetime of user data changes."
        )

class UserSchemaCreate(UserBase):
    pass

class UserSchemaUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str | None = Field(
        default=None,
        title="Username",
        description="Name of user that will be used for authentication.",
        max_length=255
        )
    password: str | None = Field(
        default=None,
        title="Password",
        description="Password of user that used for authentication.",
        max_length=255
        )
    description: str | None = Field(
        default=None, 
        title="Description", 
        description="Description of the user."
        )
    _timestamp: datetime = PrivateAttr(
        default_factory=datetime.utcnow
        )

class BookSchema(BookBase):
    author: AuthorSchema
    genres: List[GenreBase]

class BookAuthorSchema(BookBase):
    author: AuthorSchema

class AuthorSchema(AuthorBase):
    books: List[BookBase]

class GenreSchema(GenreBase):
    books: List[BookBase]

class BookGenreSchema(BookGenreBase):
    uuid: str = Field(
        default_factory=lambda: uuid_val().hex,
        title="UUID",
        description="Identifier of book genres data"
        )
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

class BookGenreUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: str | None = Field(
        default=None,
        title="Book ID", 
        description="Book identifiers."
        )
    genre_id: str | None = Field(
        default=None,
        title="Genre ID",
        description="Genre identifiers."
        )
    timestamp: datetime | None = Field(
        default=datetime.utcnow(),
        title="Timestamp",
        description="Datetime of book genre data changes."
        )

class UserSchema(UserBase):
    pass

class DeleteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message: str = Field(
        default="Data deleted successfully!"
        )

class TokenBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str

class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username: str | None = None
    scopes: list[str] = []
