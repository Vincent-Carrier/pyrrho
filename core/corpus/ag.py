from core.constants import AG
from core.ref import BCV, CV, Line
from core.treebank import GntTB, Metadata, PerseusTB

from .corpus_entry import CorpusEntry

corpus = {
    "iliad": CorpusEntry(
        Metadata(
            title="Iliad",
            author="Homer",
            writing_style="verse",
        ),
        lambda metadata: PerseusTB(
            AG / "perseus/2.1/iliad.xml", ref_cls=CV, metadata=metadata
        ),
    ),
    "persians": CorpusEntry(
        Metadata(
            title="Persians",
            author="Aeschylus",
            writing_style="verse",
        ),
        lambda metadata: PerseusTB(
            AG / "perseus/2.1/persians.xml", ref_cls=Line, metadata=metadata
        ),
    ),
    "histories": CorpusEntry(
        Metadata(
            title="Histories, Book 1",
            author="Thucydides",
        ),
        lambda metadata: PerseusTB(
            AG / "perseus/2.1/thucydides.xml", ref_cls=BCV, metadata=metadata
        ),
    ),
    "historiae": CorpusEntry(
        Metadata(
            title="Historiae, Book 1",
            author="Herodotus",
        ),
        lambda metadata: PerseusTB(
            AG / "perseus/2.1/herodotus.xml", ref_cls=BCV, metadata=metadata
        ),
    ),
    "anabasis": CorpusEntry(
        Metadata(
            title="Anabasis, Book 1",
            author="Xenophon",
        ),
        lambda metadata: PerseusTB(
            AG / "vgorman/Xen_Anab_book_1.1-5.xml",
            ref_cls=BCV,
            gorman=True,
            metadata=metadata,
        ),
    ),
    "nt": CorpusEntry(
        Metadata(
            title="New Testament",
        ),
        lambda metadata: GntTB(AG / "new-testament.conllu", metadata=metadata),
    ),
}
