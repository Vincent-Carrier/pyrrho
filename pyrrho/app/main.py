import logging
from os import environ as env

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from . import corpus
from .logger import get_logger_config

app = FastAPI()

app.include_router(corpus.router, prefix="/corpus", tags=["corpus"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/langs")
def langs():
    return {
        "langs": [
            {"id": "lat", "name": "Latin"},
            {"id": "ag", "name": "Ancient Greek"},
        ]
    }


if __name__ == "__main__":
    logger_config = get_logger_config()

    log_config = logging.basicConfig(  # type: ignore
        level=logger_config.level,
        format=logger_config.format,
        datefmt=logger_config.date_format,
        handlers=logger_config.handlers,
    )

    uvicorn.run(
        "pyrrho.app.main:app",
        reload=True,
        host="0.0.0.0",
        log_level="debug",
        use_colors=True,
        log_config=log_config,
    )