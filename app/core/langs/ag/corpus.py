from pathlib import Path

from app.core.treebanks.agldt import AgldTreebank
from app.core.treebanks.treebank import Metadata

root = Path("data/ag")

corpus = {
    "histories": AgldTreebank(
        str(root / "treebank/perseus/2.1/thucydides.xml"),
        meta=Metadata(title="Histories, Book 1", author="Thucydides"),
    ),
    "historiae": AgldTreebank(
        "treebank/perseus/2.1/herodotus.xml",
        meta=Metadata(
            title="Historiae, Book 1",
            author="Herodotus",
        ),
    ),
    "anabasis": AgldTreebank(
        str(root / "treebank/vgorman/Xen_Anab_book_1.1-5.xml"),
        meta=Metadata(title="Anabasis, Book 1", author="Xenophon"),
        gorman=True,
    ),
}
