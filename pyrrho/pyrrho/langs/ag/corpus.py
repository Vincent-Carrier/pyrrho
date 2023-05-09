from typing import Callable

from pyrrho.constants import AG
from pyrrho.nt import NT_Treebank
from pyrrho.perseus import PerseusTreebank
from pyrrho.ref import BCV
from pyrrho.treebank import Treebank

corpus: dict[str, Callable[[], Treebank]] = {
    "histories": lambda: PerseusTreebank(
        AG / "perseus/2.1/thucydides.xml",
        ref_cls=BCV,
        title="Histories, Book 1",
        author="Thucydides",
    ),
    "historiae": lambda: PerseusTreebank(
        AG / "perseus/2.1/herodotus.xml",
        ref_cls=BCV,
        title="Historiae, Book 1",
        author="Herodotus",
    ),
    "anabasis": lambda: PerseusTreebank(
        AG / "vgorman/Xen_Anab_book_1.1-5.xml",
        ref_cls=BCV,
        title="Anabasis, Book 1",
        author="Xenophon",
        gorman=True,
    ),
    "nt": lambda: NT_Treebank(
        AG / "new-testament.conllu",
        title="New Testament",
    ),
}
