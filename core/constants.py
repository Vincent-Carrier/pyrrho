import shelve
from pathlib import Path

ROOT = Path(__file__).parent.parent
BUILD = ROOT / "build"
DATA = ROOT / "data"
AG = DATA / "ag"

LSJ = lambda: shelve.open(str(AG / "lsj"))

PUNCTUATION = [".", ",", ";", ":", "·", "]", ")"]
