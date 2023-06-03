from flask import Flask, render_template
from rich import traceback

from . import routes

traceback.install()

from app.routes import corpus

app = Flask(__name__, static_url_path="/")
app.jinja_options.update(
    autoescape=False,
    auto_reload=True,
    lstrip_blocks=True,
    trim_blocks=True,
)
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")


app.register_blueprint(routes.corpus)


app.run(debug=True)
