import logging
from os import environ as env

import uvicorn
from aredis_om import Migrator
from dotenv import load_dotenv
from fastapi import FastAPI

from .logger import get_logger_config
from .routers import corpus, definitions


async def init():
    load_dotenv()
    await Migrator().run()

app = FastAPI()

app.include_router(corpus.router, prefix="/corpus", tags=["corpus"])
app.include_router(definitions.router, prefix="/definitions", tags=["definitions"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup():
    await init()


if __name__ == "__main__":
    logger_config = get_logger_config()

    log_config = logging.basicConfig( # type: ignore
        level=logger_config.level,
        format=logger_config.format,
        datefmt=logger_config.date_format,
        handlers=logger_config.handlers,
    )

    uvicorn.run(
        "app.main:app",
        reload=True,
        host="0.0.0.0",
        log_level="debug",
        use_colors=True,
        log_config=log_config
    )
