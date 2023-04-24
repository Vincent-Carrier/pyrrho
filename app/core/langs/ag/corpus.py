from pathlib import Path
from typing import NamedTuple

from app.core.treebanks.agldt import AgldTreebank
from app.core.treebanks.ref import BCV, Ref
from app.core.treebanks.treebank import Metadata

root = Path("data/ag")


class CorpusEntry(NamedTuple):
    path: str
    title: str
    author: str
    ref_type: type[Ref]
    gorman: bool = False

    def __call__(self) -> AgldTreebank:
        return AgldTreebank(
            str(root / self.path),
            Metadata(title=self.title, author=self.author),
            ref_cls=self.ref_type,
            gorman=self.gorman,
        )


corpus = {
    "histories": CorpusEntry(
        "perseus/2.1/thucydides.xml",
        title="Histories, Book 1",
        author="Thucydides",
        ref_type=BCV,
    ),
    "historiae": CorpusEntry(
        "perseus/2.1/herodotus.xml",
        title="Historiae, Book 1",
        author="Herodotus",
        ref_type=BCV,
    ),
    "anabasis": CorpusEntry(
        "vgorman/Xen_Anab_book_1.1-5.xml",
        title="Anabasis, Book 1",
        author="Xenophon",
        ref_type=BCV,
        gorman=True,
    ),
}
