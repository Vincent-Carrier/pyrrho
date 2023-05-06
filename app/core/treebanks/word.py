from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Self

from dominate.tags import span

from ..utils import cx
from .ref import RefLike


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
    def parse_agldt(cls, pos: str | None) -> Self | None:
        if pos is None:
            return None
        return _pos_agldt.get(pos)  # type: ignore
    
    @classmethod
    def parse_conll(cls, pos: str | None) -> Self | None:
        if pos is None:
            return None
        return _pos_conll.get(pos)  # type: ignore


class Case(StrEnum):
    nominative = auto()
    accusative = auto()
    dative = auto()
    genitive = auto()
    vocative = auto()

    @classmethod
    def parse_agldt(cls, case: str | None) -> Self | None:
        if case is None:
            return None
        return _case_agldt.get(case)  # type: ignore

    @classmethod
    def parse_conll(cls, case: str) -> Self | None:
        return _case_conll.get(case)  # type: ignore
    

_pos_agldt = {
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

_pos_conll = {
    "ADJ": POS.adjective,
    "ADP": POS.preposition,
    "ADV": POS.adverb,
    "AUX": POS.verb,
    "CCONJ": POS.conjunction,
    "DET": POS.article,
    "INTJ": POS.interjection,
    "NOUN": POS.noun,
    "NUM": POS.numeral,
    "PART": POS.particle,
    "PRON": POS.pronoun,
    "PROPN": POS.noun,
    "PUNCT": POS.punctuation,
    "SCONJ": POS.conjunction,
    "SYM": None,
    "VERB": POS.verb,
    "X": None,
}

_case_agldt = {
    "n": Case.nominative,
    "a": Case.accusative,
    "d": Case.dative,
    "g": Case.genitive,
    "v": Case.vocative,
    "-": None,
}

_case_conll = {
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
    definition: str | None = None
    ref: RefLike | None = None

    def render(self: Self) -> span:
        return span(
            self.form,
            cls=cx(self.case, self.pos == POS.verb and self.pos),
            data_id=str(self.id),
            data_head=str(self.head),
            data_lemma=self.lemma,
            data_flags=self.flags,
            data_def=self.definition,
        )
