from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self


class POS(StrEnum):
    noun = auto()
    verb = auto()
    participle = auto()
    adjective = auto()
    adverb = auto()
    article = auto()
    particle = auto()
    conjunction = auto()
    preposition = auto()
    pronoun = auto()
    numeral = auto()
    interjection = auto()
    exclamation = auto()
    punctuation = auto()

    @classmethod
    def parse_tag(cls, pos: str | None) -> Self | None:
        if pos is None:
            return None
        return _pos_tags.get(pos)  # type: ignore


class Case(StrEnum):
    nominative = auto()
    accusative = auto()
    dative = auto()
    genitive = auto()
    vocative = auto()

    @classmethod
    def parse_tag(cls, case: str | None) -> Self | None:
        if case is None:
            return None
        return _case_tags.get(case)  # type: ignore

    @classmethod
    def parse_feat(cls, case: str) -> Self | None:
        return _case_feats.get(case)  # type: ignore


_pos_tags = {
    "n": POS.noun,
    "v": POS.verb,
    "t": POS.participle,
    "a": POS.adjective,
    "d": POS.adverb,
    "l": POS.article,
    "g": POS.particle,
    "c": POS.conjunction,
    "r": POS.preposition,
    "p": POS.pronoun,
    "m": POS.numeral,
    "i": POS.interjection,
    "e": POS.exclamation,
    "u": POS.punctuation,
    "-": None,
}

_case_tags = {
    "n": Case.nominative,
    "a": Case.accusative,
    "d": Case.dative,
    "g": Case.genitive,
    "v": Case.vocative,
    "-": None,
}

_case_feats = {
    "Nom": Case.nominative,
    "Acc": Case.accusative,
    "Dat": Case.dative,
    "Gen": Case.genitive,
    "Voc": Case.vocative,
}


@dataclass
class Word:
    form: str
    id: int | None
    head: int | None
    lemma: str | None
    pos: POS | None
    case: Case | None
    flags: str | None = None
