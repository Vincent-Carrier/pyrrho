from flask import Flask, render_template
from livereload import Server
from rich import traceback

from . import routes

traceback.install()


app = Flask(__name__, static_url_path="/")
app.jinja_options.update(
    autoescape=False,
    lstrip_blocks=True,
    trim_blocks=True,
)
app.debug = True


@app.route("/")
def index():
    return render_template("index.html")


app.register_blueprint(routes.corpus)
app.register_blueprint(routes.fonts)
app.register_blueprint(routes.shoelace)

server = Server(app)
server.watch("app/templates/**.html")
server.watch("app/static/**.css")
server.watch("app/static/**.js")
server.serve(port=5000)
