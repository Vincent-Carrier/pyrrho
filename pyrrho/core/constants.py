import shelve
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
AG = DATA / "ag"

LSJ = lambda: shelve.open(str(AG / "lsj"))
