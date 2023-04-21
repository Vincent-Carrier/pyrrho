from os import environ as env

from fastapi import FastAPI

from app import init
from app.routers import corpus, definitions

app = FastAPI()

app.include_router(corpus.router, prefix="/corpus", tags=["corpus"])
app.include_router(definitions.router, prefix="/definitions", tags=["definitions"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup():
    await init()
