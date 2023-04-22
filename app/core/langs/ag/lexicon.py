import re
from pathlib import Path

from lxml import etree

from app.core.lexicon import LexiconEntry

# class LsjEntry(LexiconEntry):
#     definitions: list[str]

TRAILING_REGEX = re.compile(r"(\s|\.|,|;)+$")


async def seed_lsj():
    print("Seeding LSJ...")
    for p in Path("data/ag/lsj").glob("*.xml"):
        print(f"Processing {p}...")
        root = etree.parse(p.as_posix()).getroot()
        for entry in root.findall(".//entryFree"):
            lemma = entry.attrib["key"]
            definitions = [re.sub(TRAILING_REGEX, "", e.text) for e in entry.findall(".//tr") if e.text] # type: ignore
            if len(definitions) > 0:
                await LexiconEntry(lemma=lemma, definitions=definitions).save()
