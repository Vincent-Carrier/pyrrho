from pathlib import Path

from app.core.treebanks.agldt import AgldTreebank
from app.core.treebanks.treebank import Metadata

root = Path("data/ag/treebank")

corpus = {
    "histories": AgldTreebank(
        str(root / "perseus/2.1/thucydides.xml"),
        Metadata(title="Histories, Book 1", author="Thucydides"),
    ),
    "historiae": AgldTreebank(
        "perseus/2.1/herodotus.xml",
        Metadata(title="Historiae, Book 1", author="Herodotus"),
    ),
    "anabasis": AgldTreebank(
        str(root / "vgorman/Xen_Anab_book_1.1-5.xml"),
        Metadata(title="Anabasis, Book 1", author="Xenophon"),
        gorman=True,
    ),
}
