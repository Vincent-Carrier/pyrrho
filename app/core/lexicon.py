from typing import NamedTuple


class LexiconEntry(NamedTuple):
    lemma: str
    definitions: list[str]
