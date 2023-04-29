import csv
import re
import shelve
from itertools import islice

TRAILING_REGEX = re.compile(r"(\s|\.|,|;)+$")


async def seed_lsj():
    print("Seeding LSJ...")
    with open ("data/ag/LSJ_shortdefs.tsv") as f:
        with shelve.open("data/ag/lsj") as db:
            for [lemma, definition] in csv.reader(f, dialect="excel-tab"):
                db[lemma] = definition # TODO: normalize

            print(f"Sample: {list(islice(db.items(), 5))}")
