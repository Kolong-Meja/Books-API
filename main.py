# app/main.py

"""Main program of this project."""

import os
import uvicorn

from fastapi import FastAPI
from app.routes import router
from dotenv import load_dotenv


# include the tags metadata.
tags_metadata = [
    {
        "name": "books",
        "description": "--|Operations with books|--"
    },
    {
        "name": "authors",
        "description": "--|Operations with authors|--"
    },
    {
        "name": "genres",
        "description": "--|Operations with genres|--"
    },
    {
        "name": "book_genres",
        "description": "--|Operations with book genres|--"
    },
]

# define the app.
app = FastAPI(
    title="Books API", 
    description="Is an API to create, get, view and manage all data related to Books. You can be as free as possible to do all that here.", 
    summary="This use for manage Books data.", 
    debug=True,
    version="1.0.0",
    openapi_tags=tags_metadata,
    separate_input_output_schemas=False)
app.include_router(router)

# load all variable from env file.
load_dotenv()

# get host and port from env file.
dev_host = os.environ.get("APP_DEV_HOST")
dev_port = int(os.environ.get("APP_DEV_PORT"))

# run the program.
if __name__ == "__main__":
    uvicorn.run("__main__:app", host=dev_host, port=dev_port, use_colors=True, reload=True)
