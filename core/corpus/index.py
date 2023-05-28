from dataclasses import replace
from typing import Iterator, NamedTuple, NewType

from core.treebank import Metadata

from .ag import corpus as ag_corpus
from .corpus_entry import CorpusEntry


LangId = NewType("LangId", str)

class LangEntry(NamedTuple):
    name: str
    corpus: dict[DocId, CorpusEntry]


langs = {
    LangId("ag"): LangEntry("Ancient Greek", ag_corpus),
}


def index(lang: str | None = None) -> dict[str, Metadata]:
    if lang:
        return {slug: meta for slug, (meta, _) in langs[lang].corpus.items()}
    else:
        return {
            slug: replace(meta, lang=lang_slug)
            for lang_slug, lang in langs.items()
            for slug, (meta, _) in lang.corpus.items()
        }


def all_treebanks() -> Iterator[CorpusEntry]:
