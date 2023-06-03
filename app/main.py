import logging

from flask import Flask
from rich.logging import RichHandler

from app.routes import corpus

app = Flask(__name__)
app.jinja_options.update(
    lstrip_blocks=True,
    trim_blocks=True,
)

app.register_blueprint(corpus.bp, url_prefix="/corpus")
app.include_router(corpus.router, prefix="/corpus", tags=["corpus"])

app.mount("/", StaticFiles(directory="static"), name="static")


@app.route("/")
async def root():
    return RedirectResponse("/docs")


@app.route("/langs")
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
