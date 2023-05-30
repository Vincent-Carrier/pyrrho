from functools import cache

from core.corpus.corpus_entry import DocId
from core.treebank import Metadata, Treebank

from .index import LangId, langs


@cache
def get_treebank(lang: LangId, slug: DocId) -> Treebank:
    _, corpus = langs[lang]
    return corpus[slug]()


def get_metadata(lang: LangId, slug: DocId) -> Metadata:
    _, corpus = langs[lang]
    return corpus[slug].metadata
