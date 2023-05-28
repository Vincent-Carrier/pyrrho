import shelve
from os import environ as ENV
from pathlib import Path

from jinja2 import Environment, PackageLoader

ROOT = Path(__file__).parent.parent
BUILD = ROOT / "build"
DATA = ROOT / "data"
AG = DATA / "ag"

PUNCTUATION = [".", ",", ";", ":", "·", "]", ")"]

LSJ = lambda: shelve.open(str(AG / "lsj"))

jinja = Environment(loader=PackageLoader("core.render", "templates"))
