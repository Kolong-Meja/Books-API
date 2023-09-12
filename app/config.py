# app/config.py

"""App configuration place."""

import os

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


# load all variable from env file.
load_dotenv()

# define the databases.
postgres_db = os.getenv("POSTGRES_DATABASE_URL")
sqlite_db = os.path.join(Path.cwd(), "books.db")

# throw all your configuration variable in here!
SQLALCHEMY_DATABASE_URL = f"sqlite:///{sqlite_db}"

# create connection between app and database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

# create session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# define the base.
Base = declarative_base()

# for authentication purpose.
SECRET_KEY = os.environ.get("SECRET_KEY")
REFRESH_KEY = os.environ.get("REFRESH_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/token")

# get host and port from env file.
DEV_HOST = os.environ.get("APP_DEV_HOST")
DEV_PORT = int(os.environ.get("APP_DEV_PORT"))

# dependency.
def get_database():
    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()
    
# feature for API
app_description = """
Is a Restful API for managing book data, etc. \
Here you can CREATE, UPDATE, DELETE, and READ all data related to the book. \
For the record, each endpoint does not always return a UUID or ID (string), \
this is done for data security. However, there are some endpoints that must use UUID or ID (string) from data, \
so you can check these specific endpoints.

Endpoints that respond to UUID returns include:
- **GET /api/book/{title}**
- **POST /api/book_genres**
- **GET /api/book_genres**
- **PATCH /api/book_genres/{book_genre_id}**

This Restful API also fully supports the use of Access Tokens for Authorization or Authentication. \
There are several endpoints that require an Access Token, most of which are all endpoints under the **book_genres** label. \
So pay close attention to each endpoint whether it requires an Access Token or not.
"""

# include the tags metadata.
tags_metadata = [
    {
        "name": "books",
        "description": "Operations with books"
    },
    {
        "name": "authors",
        "description": "Operations with authors"
    },
    {
        "name": "genres",
        "description": "Operations with genres"
    },
    {
        "name": "book_genres",
        "description": "Operations with book genres"
    },
    {
        "name": "users",
        "description": "Operations with users"
    },
    {
        "name": "authentications",
        "description": "Operations with authentications"
    }
]