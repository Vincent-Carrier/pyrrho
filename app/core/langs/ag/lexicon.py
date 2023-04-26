import re
import shelve
from itertools import islice
from pathlib import Path

from lxml import etree

from app.core.lexicon import LexiconEntry

TRAILING_REGEX = re.compile(r"(\s|\.|,|;)+$")


async def seed_lsj():
    print("Seeding LSJ...")
    for p in Path("data/ag/lsj").glob("*.xml"):
        print(f"Processing {p}...")
        root = etree.parse(p.as_posix()).getroot()
        with shelve.open("data/ag/lsj.db") as db:
            for entry in root.findall(".//entryFree"):
                lemma = str(entry.attrib["key"])
                definitions = [
                    re.sub(TRAILING_REGEX, "", e.text)
                    for e in entry.findall(".//tr")
                    if e.text
                ]
                if len(definitions) > 0:
                    db[lemma] = LexiconEntry(lemma, definitions)

        print(f"Sample: {list(islice(db.items(), 5))}")
