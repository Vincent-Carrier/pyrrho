import csv
import re
from itertools import islice

from core.constants import AG, LSJ

TRAILING_REGEX = re.compile(r"(\s|\.|,|;)+$")


print("Seeding LSJ...")
with open(AG / "LSJ_shortdefs.tsv") as f:
    with LSJ() as db:
        for [lemma, definition] in csv.reader(f, dialect="excel-tab"):
            db[lemma] = definition  # TODO: normalize
        print(f"Sample: {list(islice(db.items(), 5))}")
