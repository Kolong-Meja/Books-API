# app/routes.py

"""App routes place."""

from fastapi import (
    Depends, 
    APIRouter,
    status,
    )
from sqlalchemy.orm import Session
from app import schemas
from app.config import get_database
from app.controllers import (
    author_controller,
    book_controller, 
    genre_controller,
    book_genre_controller,
    user_controller,
    authentication_controller
    )
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.controllers.authentication_controller import get_current_user


# define route.
router = APIRouter()

"""
BOOKS ROUTES!
"""
# NOTE: for response_model argument, use schemas!
@router.get("/api/books", 
         response_model=list[schemas.BookSchema], 
         tags=["books"],
         deprecated=False,
         summary="Read or get all books data.",
         status_code=status.HTTP_200_OK
         )
def read_books(session: Session = Depends(get_database), skip: int = 0, limit: int = 100,):
    """
    Read or get all books data and paginate the data's with skip and limit query.

    **Parameters**:
    - **skip**: Skip certain number of item before returning the items. Default = 0.
    - **limit**: Maximum number of items to be returned. Default = 100.
    """
    return book_controller.get_all_books(
        session=session,
        skip=skip,
        limit=limit
        )

# NOTE: for response_model argument, use schemas!
@router.post("/api/book", 
          response_model=schemas.BookBase, 
          tags=["books"],
          deprecated=False,
          summary="Create one new book data.",
          status_code=status.HTTP_201_CREATED
          )
def create_book(author_id: str, book: schemas.BookSchemaCreate, session: Session = Depends(get_database)):
    """
    Create one book data and create relationship with author.

    **Parameter**:
    - **author_id**: Identifier of author to be connected.
    """
    return book_controller.create_book(
        author_id=author_id,
        book=book,
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.get("/api/book/{title}", 
         response_model=schemas.BookSchema, 
         tags=["books"],
         deprecated=False,
         summary="Read or get one book data base on book title.",
         status_code=status.HTTP_200_OK
         )
def read_book(title: str, session: Session = Depends(get_database)):
    """
    Read or get one book base on book title.

    **Parameter**:
    - **title**: The title name of the book to be returned.
    """
    return book_controller.get_book(
        title=title, 
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.patch("/api/book/{title}", 
           response_model=schemas.BookBase, 
           tags=["books"], 
           deprecated=False,
           summary="Update book data base on book title.",
           status_code=status.HTTP_200_OK
           )
def update_book(title: str, book: schemas.BookSchemaUpdate, session: Session = Depends(get_database)):
    """
    Update one book data base on book title.

    **Parameter**:
    - **title**: The title name of the book to be returned.
    """
    return book_controller.update_book(
        title=title, 
        book=book,
        session=session
        )

@router.delete("/api/book/{title}",
            response_model=schemas.DeleteSchema,
            tags=["books"], 
            deprecated=False,
            summary="Delete one book data base on book title.",
            status_code=status.HTTP_200_OK
            )
def delete_book(title: str, session: Session = Depends(get_database)):
    """
    Delete one book data base on book title.

    **Parameter**:
    - **title**: The title name of the book to be deleted.
    """
    return book_controller.delete_book(
        title=title,
        session=session
        )

@router.put("/api/book/{title}/author",
              response_model=schemas.BookAuthorSchema,
              tags=["books"],
              deprecated=False,
              summary="Change author by book title",
              status_code=status.HTTP_200_OK
              )
def update_author_by_book(title: str, book: schemas.BookAuthorSchemaUpdate, session: Session = Depends(get_database)):
    """
    Change author by book title.

    **NOTE**: Use this if the book's author data in the book's data is not the author of the book.

    **Parameter**
    - **title**: The title name of the book.
    """
    return book_controller.update_author_by_title(
        title=title,
        book=book,
        session=session
        )

"""
AUTHORS ROUTES!
"""
# NOTE: for response_model argument, use schemas!
@router.get("/api/authors", 
         response_model=list[schemas.AuthorSchema], 
         tags=["authors"],
         deprecated=False,
         summary="Read or get all authors data."
         )
def read_authors(session: Session = Depends(get_database), skip: int = 0, limit: int = 100):
    """
    Read or get all authors data and paginate the data's with skip and limit query.

    **Parameters**:
    - **skip**: Skip certain number of item before returning the items. Default = 0.
    - **limit**: Maximum number of items to be returned. Default = 100.
    """
    return author_controller.get_all_authors(
        session=session, 
        skip=skip,
        limit=limit)

# NOTE: for response_model argument, use schemas!
@router.post("/api/author", 
          response_model=schemas.AuthorBase, 
          tags=["authors"],
          deprecated=False,
          summary="Create one author data."
          )
def create_author(author: schemas.AuthorSchemaCreate, session: Session = Depends(get_database)):
    """
    Create one author data.
    """
    return author_controller.create_author(
        author=author,
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.get("/api/author/{name}", 
         response_model=schemas.AuthorSchema, 
         tags=["authors"],
         deprecated=False,
         summary="Read or get one author data base on author name."
         )
def read_author(name: str, session: Session = Depends(get_database)):
    """
    Read or get one author data base on author name.

    **Parameter**:
    - **name**: The name of author to be returned.
    """
    return author_controller.get_author(
        name=name,
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.patch("/api/author/{name}", 
           response_model=schemas.AuthorBase, 
           tags=["authors"], 
           deprecated=False,
           summary="Update one author data base on author name."
           )
def update_author(name: str, author: schemas.AuthorSchemaUpdate, session: Session = Depends(get_database)):
    """
    Update or change one author data base on author name.

    **Parameter**:
    - **name**: The name of author to be returned.
    """
    return author_controller.update_author(
        name=name,
        author=author,
        session=session
        )

@router.delete("/api/author/{name}", 
            response_model=schemas.DeleteSchema,
            tags=["authors"], 
            deprecated=False,
            summary="Delete one author data base on author name.",
            status_code=status.HTTP_200_OK
            )
def delete_author(name: str, session: Session = Depends(get_database)):
    """
    Delete on author data base on author name.

    **Parameter**:
    - **name**: The name of author to be deleted.
    """
    return author_controller.delete_author(
        name=name, 
        session=session
        )

"""
GENRES ROUTES!
"""
# NOTE: for response_model argument, use schemas!
@router.get("/api/genres", 
         response_model=list[schemas.GenreSchema],
         tags=["genres"],
         deprecated=False,
         summary="Read or get all genres book data."
         )
def read_genres(session: Session = Depends(get_database), skip: int = 0, limit: int = 100):
    """
    Read or get all genres data and paginate the data's with skip and limit query.

    **Parameters**:
    - **skip**: Skip certain number of item before returning the items. Default = 0.
    - **limit**: Maximum number of items to be returned. Default = 100.
    """
    return genre_controller.get_genres(
        session=session,
        skip=skip,
        limit=limit
        )

# NOTE: for response_model argument, use schemas!
@router.post("/api/genre", 
          response_model=schemas.GenreBase,
          tags=["genres"],
          deprecated=False,
          summary="Create one genre data.")
def create_genre(genre: schemas.GenreSchemaCreate, session: Session = Depends(get_database)):
    """
    Create one genre data.
    """
    return genre_controller.create_genre(
        genre=genre, 
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.get("/api/genre/{name}",
            response_model=schemas.GenreSchema,
            tags=["genres"],
            deprecated=False,
            summary="Read or get one genre data.",
            status_code=status.HTTP_200_OK
            )
def read_genre(name: str, session: Session = Depends(get_database)):
    """
    Read or get one genre data.

    **Parameter**:
    - **name**: The name of genre to be returned.
    """
    return genre_controller.get_genre(
        name=name, 
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.patch("/api/genre/{name}",
              response_model=schemas.GenreBase,
              tags=["genres"],
              deprecated=False,
              summary="Update one genre data.",
              status_code=status.HTTP_200_OK
              )
def update_genre(name: str, genre: schemas.GenreSchemaUpdate, session: Session = Depends(get_database)):
    """
    Update or change one genre data.

    **Parameter**:
    - **name**: The name of genre to be returned.
    """
    return genre_controller.update_genre(
        name=name, 
        genre=genre, 
        session=session
        )

@router.delete("/api/genre/{name}",
               response_model=schemas.DeleteSchema,
               tags=["genres"],
               deprecated=False,
               summary="Delete one genre data.",
               status_code=status.HTTP_200_OK
               )
def delete_genre(name: str, session: Session = Depends(get_database)):
    """
    Delete one genre data.

    **Parameter**:
    - **name**: The name of genre to be deleted.
    """
    return genre_controller.delete_genre(
        name=name, 
        session=session
        )

"""
BOOK GENRES ROUTES!
"""
# NOTE: for response_model argument, use schemas!
@router.post("/api/book_genres",
          response_model=schemas.BookGenreSchema,
          tags=["book_genres"],
          deprecated=False,
          summary="Create relationship between Books and Genres.",
          status_code=status.HTTP_201_CREATED
          )
def create_book_genres(
    book_genre: schemas.BookGenreSchema, 
    session: Session = Depends(get_database),
    auth: schemas.UserSchema = Depends(get_current_user)
    ):
    """
    **WARNING**: This endpoint needs access token, make sure you have an access token.

    Create relationship between Books and Genres.

    **NOTE**: Use this if book data and genre data have already been filled in or created.
    """
    return book_genre_controller.create_book_genres(
        auth=auth,
        book_genre=book_genre,
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.get("/api/book_genres",
            response_model=list[schemas.BookGenreSchema],
            tags=["book_genres"],
            deprecated=False,
            summary="Read or get all book genres data.",
            status_code=status.HTTP_200_OK
            )
def read_book_genres(
    auth: schemas.UserSchema = Depends(get_current_user),
    session: Session = Depends(get_database), 
    skip: int = 0, 
    limit: int = 100, 
    ):
    """
    **WARNING**: This endpoint needs access token, make sure you have an access token.

    Read or get all book genres data and paginate the data's with skip and limit query.

    **Parameters**:
    - **skip**: Skip certain number of item before returning the items. Default = 0.
    - **limit**: Maximum number of items to be returned. Default = 100.
    """
    return book_genre_controller.get_all_book_genres(
        auth=auth,
        session=session,
        skip=skip,
        limit=limit
        )

# NOTE: for response_model argument, use schemas!
@router.get("/api/book_genres/book/{book_id}",
            response_model=schemas.BookSchema,
            tags=["book_genres"],
            deprecated=False,
            summary="Read or get one book data base on book id",
            status_code=status.HTTP_200_OK
            )
def read_book(
    book_id: str, 
    session: Session = Depends(get_database),
    auth: schemas.UserSchema = Depends(get_current_user)
    ):
    """
    **WARNING**: This endpoint needs access token, make sure you have an access token.

    Read or get book data using a JOIN statement with the BookGenres model. This endpoint requires book_id as a parameter.

    **Parameter**:
    - **book_id**: Identifier of book.
    """
    return book_genre_controller.get_book_data(
        auth=auth,
        book_id=book_id,
        session=session
        )

# NOTE: for response_model argument, use schemas!
@router.get("/api/book_genres/genre/{genre_id}",
            response_model=schemas.GenreSchema,
            tags=["book_genres"],
            deprecated=False,
            summary="Read or get one genre data base on genre id",
            status_code=status.HTTP_200_OK
            )
def read_book(
    genre_id: str, 
    session: Session = Depends(get_database),
    auth: schemas.UserSchema = Depends(get_current_user)
    ):
    """
    **WARNING**: This endpoint needs access token, make sure you have an access token.

    Read or get genre data using a JOIN statement with the BookGenres model. This endpoint requires genre_id as a parameter.

    **Parameter**:
    - **genre_id**: Identifier of genre.
    """
    return book_genre_controller.get_genre_data(
        auth=auth,
        genre_id=genre_id,
        session=session
        )

"""
USER ROUTES!
"""
@router.get("/api/users", 
            response_model=list[schemas.UserSchema],
            tags=["users"],
            deprecated=False,
            summary="Read or get users data.",
            status_code=status.HTTP_200_OK
            )
def read_users(
    session: Session = Depends(get_database), 
    skip: int = 0, 
    limit: int = 100
    ):
    return user_controller.get_all_users(
        session=session, 
        skip=skip, 
        limit=limit
        )

@router.post("/api/user", 
             response_model=schemas.UserSchema, 
             tags=["users"], 
             deprecated=False, 
             summary="Create one user data.", 
             status_code=status.HTTP_201_CREATED
             )
def create_user(
    user: schemas.UserSchemaCreate, 
    session: Session = Depends(get_database)
    ):
    return user_controller.create_user(
        user=user, 
        session=session
        )

@router.get("/api/user/{username}", 
            response_model=schemas.UserSchema, 
            tags=["users"], 
            deprecated=False, 
            summary="Read or get one user data base on username.",
            status_code=status.HTTP_200_OK
            )
def read_user(username: str, session: Session = Depends(get_database)):
    return user_controller.get_user(
        username=username, 
        session=session
        )

@router.patch("/api/user/{username}", 
              response_model=schemas.UserSchema, 
              tags=["users"], 
              deprecated=False, 
              summary="Update one user data base on username.", 
              status_code=status.HTTP_200_OK
              )
def update_user(
    username: str, 
    user: schemas.UserSchemaUpdate, 
    session: Session = Depends(get_database)
    ):
    return user_controller.update_user(
        username=username, 
        user=user, 
        session=session
        )

@router.delete("/api/user/{username}", 
            response_model=schemas.DeleteSchema, 
            tags=["users"],
            deprecated=False,
            summary="Delete one user data.",
            status_code=status.HTTP_200_OK
            )
def delete_user(username: str, session: Session = Depends(get_database)):
    return user_controller.delete_user(
        username=username, 
        session=session
        )

"""
AUTH ROUTES!
"""
@router.post("/api/token", 
             response_model=schemas.TokenBase, 
             tags=["authentications"], 
             deprecated=False,
             status_code=status.HTTP_200_OK,
             summary="Create one access token."
             )
def access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    session: Session = Depends(get_database)
    ):
    """
    Create access token for execute protected routes.

    **NOTE**: Make sure to input registered username and password.
    """
    return authentication_controller.get_access_token(
        form_data=form_data, 
        session=session
        )

