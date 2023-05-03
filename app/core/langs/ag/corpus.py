from pathlib import Path
from typing import Callable

from ...treebanks.nt import NT_Treebank
from ...treebanks.perseus import PerseusTreebank
from ...treebanks.ref import BCV
from ...treebanks.treebank import Treebank

root = Path("data/ag")


corpus: dict[str, Callable[[], Treebank]] = {
    "histories": lambda: PerseusTreebank(
        root / "perseus/2.1/thucydides.xml",
        ref_cls=BCV,
        title="Histories, Book 1",
        author="Thucydides",
    ),
    "historiae": lambda: PerseusTreebank(
        root / "perseus/2.1/herodotus.xml",
        ref_cls=BCV,
        title="Historiae, Book 1",
        author="Herodotus",
    ),
    "anabasis": lambda: PerseusTreebank(
        root / "vgorman/Xen_Anab_book_1.1-5.xml",
        ref_cls=BCV,
        title="Anabasis, Book 1",
        author="Xenophon",
        gorman=True,
    ),
    "nt": lambda: NT_Treebank(
        root / "new-testament.conllu",
        title="New Testament",
    ),
}
