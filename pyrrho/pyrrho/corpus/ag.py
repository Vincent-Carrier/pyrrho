from typing import Callable

from pyrrho import nt, perseus
from pyrrho.constants import AG
from pyrrho.ref import BCV
from pyrrho.treebank import Treebank

corpus: dict[str, Callable[[], Treebank]] = {
    "histories": lambda: perseus.TB(
        AG / "perseus/2.1/thucydides.xml",
        ref_cls=BCV,
        title="Histories, Book 1",
        author="Thucydides",
    ),
    "historiae": lambda: perseus.TB(
        AG / "perseus/2.1/herodotus.xml",
        ref_cls=BCV,
        title="Historiae, Book 1",
        author="Herodotus",
    ),
    "anabasis": lambda: perseus.TB(
        AG / "vgorman/Xen_Anab_book_1.1-5.xml",
        ref_cls=BCV,
        title="Anabasis, Book 1",
        author="Xenophon",
        gorman=True,
    ),
    "nt": lambda: nt.TB(
        AG / "new-testament.conllu",
        title="New Testament",
    ),
}
