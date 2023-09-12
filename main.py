# app/main.py

"""Main program of this project."""

import os
import uvicorn

from fastapi import FastAPI
from app.routes import router
from dotenv import load_dotenv
from app.config import (
    app_description,
    tags_metadata,
    DEV_HOST, 
    DEV_PORT
    )

# define the app.
app = FastAPI(
    title="Books REST API", 
    description=app_description, 
    summary="This use for manage Books data.", 
    debug=True,
    version="1.0.0",
    openapi_tags=tags_metadata,
    separate_input_output_schemas=False,
    license_info={
        "name": "GNU General Public License version 3",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html"
        },
    )
app.include_router(router)

# run the program.
if __name__ == "__main__":
    uvicorn.run("__main__:app", host=DEV_HOST, port=DEV_PORT, use_colors=True, reload=True)
