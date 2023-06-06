import os
import shelve
from pathlib import Path

from box import Box

ENV = Box(os.environ)
ROOT = Path(__file__).parent
BUILD = ROOT / "build"
DATA = ROOT / "data"
NODE_MODULES = ROOT / "node_modules"
AG = DATA / "ag"

PUNCTUATION = [".", ",", ";", ":", "·", "]", ")"]

LSJ = lambda: shelve.open(str(AG / "lsj"))
