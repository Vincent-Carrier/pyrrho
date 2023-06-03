from flask import Flask
from rich import traceback

traceback.install()

from app.routes import corpus

app = Flask(__name__, static_url_path="/")
app.jinja_options.update(
    autoescape=False,
    lstrip_blocks=True,
    trim_blocks=True,
)

app.register_blueprint(corpus.bp, url_prefix="/corpus")


@app.route("/langs")
def langs():
    return {
        "langs": [
            {"id": "lat", "name": "Latin"},
            {"id": "ag", "name": "Ancient Greek"},
        ]
    }


app.run(debug=True)
