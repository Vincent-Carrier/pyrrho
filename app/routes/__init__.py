import stat

from flask import Blueprint

from constants import NODE_MODULES

from .corpus import bp as corpus

fonts = Blueprint(
    "fonts",
    __name__,
    static_folder=str(NODE_MODULES / "@fontsource/"),
    static_url_path="/fonts",
)
shoelace = Blueprint(
    "shoelace",
    __name__,
    static_folder=str(NODE_MODULES / "@shoelace-style/shoelace/dist/"),
    static_url_path="/shoelace",
)
