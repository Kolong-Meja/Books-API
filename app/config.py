# app/config.py

"""App configuration place."""

import os

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext


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
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
