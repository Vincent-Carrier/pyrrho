import re
from dataclasses import dataclass
from enum import StrEnum, auto
from typing import Literal, Self

import lookup
from utils import at


@dataclass
class Location:
    book: int
    verse: int


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


pos_tags = {
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


class Case(StrEnum):
    nominative = auto()
    accusative = auto()
    dative = auto()
    genitive = auto()
    vocative = auto()


case_tags = {
    "n": Case.nominative,
    "a": Case.accusative,
    "d": Case.dative,
    "g": Case.genitive,
    "v": Case.vocative,
    "-": None,
}


@dataclass
class Word:
    id: int | None
    head: int | None
    form: str | None
    lemma: str | None
    definition: str | None
    pos: POS | None
    case: Case | None
    flags: str | None
    loc: Location | None


def parse_word(attr: dict) -> Word | None:
    if attr.get("insertion_id") is not None:
        return None

    tags = attr.get("postag")
    pos = at(tags, 0)
    case = at(tags, 7)

    location = None
    if attr.get("cite"):
        match = re.search(
            r"urn:cts:greekLit:tlg\d{4}.tlg\d{3}:(\d+)\.(\d+)", attr["cite"]
        )
        if match:
            book, verse = int(match.group(1)), int(match.group(2))
            location = Location(book, verse)

    lemma = attr.get("lemma")
    if lemma:
        lemma = re.sub(r"\d+$", "", lemma)
    definition = lookup.lsj.get(lemma)
    if definition:
        definition = re.sub(r"\W+$", "", definition)

    def parse_int(s: str | None) -> int | None:
        if s is None:
            return None
        return int(s) if s != "" else None

    return Word(
        id=parse_int(attr.get("id")),
        head=parse_int(attr.get("head")),
        form=attr.get("form"),
        lemma=lemma,
        definition=definition,
        pos=pos,
        case=case,
        flags=tags,
        loc=location,
    )
