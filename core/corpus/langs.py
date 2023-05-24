from typing import NamedTuple

from core.treebank import Metadata

from .ag import corpus as ag_corpus
from .corpus_entry import CorpusEntry


class LangEntry(NamedTuple):
    name: str
    corpus: dict[str, CorpusEntry]


langs = {
    "ag": LangEntry("Ancient Greek", ag_corpus),
}


def index(lang: str | None = None) -> dict[str, Metadata]:
    if lang:
        return {slug: meta for slug, (meta, _) in langs[lang].corpus.items()}
    else:
        return {
            slug: meta
            for _, lang in langs.items()
            for slug, (meta, _) in lang.corpus.items()
        }
