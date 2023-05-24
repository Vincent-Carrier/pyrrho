from functools import cache

from core.treebank import Metadata, Treebank

from .index import langs


@cache
def get_treebank(lang: str, slug: str) -> Treebank:
    _, corpus = langs[lang]
    return corpus[slug]()


def get_metadata(lang: str, slug: str) -> Metadata:
    _, corpus = langs[lang]
    return corpus[slug].metadata
