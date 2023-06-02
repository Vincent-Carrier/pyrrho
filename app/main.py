import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from rich.logging import RichHandler

from app import corpus

app = FastAPI()

app.include_router(corpus.router, prefix="/corpus", tags=["corpus"])

app.mount("/", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse("/docs")


@app.get("/langs")
def langs():
    return {
        "langs": [
            {"id": "lat", "name": "Latin"},
            {"id": "ag", "name": "Ancient Greek"},
        ]
    }


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s \t%(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True)],
)

uvicorn.run(
    "app.main:app",
    port=8888,
    reload=True,
    log_level="debug",
    use_colors=True,
)
