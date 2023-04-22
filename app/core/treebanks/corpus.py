import re
from os import makedirs
from pathlib import Path

from treebank import AGD_Treebank, Metadata

corpus = [
    AGD_Treebank(
        "treebank/perseus/2.1/thucydides.xml",
        meta=Metadata(title="Histories, Book 1", author="Thucydides", slug="histories"),
    ),
    AGD_Treebank(
        "treebank/perseus/2.1/herodotus.xml",
        meta=Metadata(
            title="Historiae, Book 1",
            author="Herodotus",
            slug="historiae",
            book="1",
        ),
    ),
    AGD_Treebank(
        "treebank/vgorman/Xen_Anab_book_1.1-5.xml",
        meta=Metadata(title="Anabasis, Book 1", author="Xenophon", slug="anabasis"),
        gorman=True,
    ),
]

outdir = Path("/Users/vincent/Code/vcar.dev.astro/src/content/treebank")

for tb in corpus:
    dir = outdir / re.sub(" ", "-", tb.meta.author.lower()) / tb.meta.slug.lower()
    makedirs(dir, exist_ok=True)
    for chunk in tb.chunks(10):
        with open(dir / f"{chunk.id}.md", "w") as f:
            print(f"writing to {f.name}")
            f.write(tb.render_chunk(chunk))
