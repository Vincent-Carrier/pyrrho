from enum import Enum, auto
from typing import TypeAlias

from .ref import RefPoint
from .word import Word


class FormatToken(Enum):
    SENTENCE_START = auto()
    SENTENCE_END = auto()
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()
    LINE_BREAK = auto()


FT = FormatToken

Token: TypeAlias = Word | RefPoint | FormatToken

PUNCTUATION = [".", ",", ";", ":", "·", "]", ")"]
