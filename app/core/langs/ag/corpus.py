from pathlib import Path

from app.core.treebanks.agldt import AgldTreebank
from app.core.treebanks.ref import BCV, CV
from app.core.treebanks.treebank import Metadata

root = Path("data/ag")

corpus = {
    "histories": AgldTreebank(
        str(root / "perseus/2.1/thucydides.xml"),
        Metadata(title="Histories, Book 1", author="Thucydides"),
        ref_cls=BCV,
    ),
    "historiae": AgldTreebank(
        str(root/"perseus/2.1/herodotus.xml"),
        Metadata(title="Historiae, Book 1", author="Herodotus"),
        ref_cls=BCV,
    ),
    "anabasis": AgldTreebank(
        str(root / "vgorman/Xen_Anab_book_1.1-5.xml"),
        Metadata(title="Anabasis, Book 1", author="Xenophon"),
        ref_cls=BCV,
        gorman=True,
    ),
}
