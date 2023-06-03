from typing import NamedTuple, NewType

from core.treebank import Metadata, Treebank

from .ag import corpus as ag_corpus
from .corpus_entry import CorpusEntry, DocId

LangId = NewType("LangId", str)


class LangEntry(NamedTuple):
    name: str
    corpus: dict[DocId, CorpusEntry]


langs = {
    LangId("ag"): LangEntry("Ancient Greek", ag_corpus),
}


def index(lang: LangId | None = None) -> dict[str, Metadata]:
    if lang:
        return {slug: meta for slug, (meta, _) in langs[lang].corpus.items()}
    else:
        return {
            slug: meta
            for _, lang in langs.items()
            for slug, (meta, _) in lang.corpus.items()
        }


def all_treebanks() -> dict[DocId, Treebank]:
    return {
        slug: entry()
        for _, lang in langs.items()
        for slug, entry in lang.corpus.items()
    }
