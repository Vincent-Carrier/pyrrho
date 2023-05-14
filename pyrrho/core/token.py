from enum import Enum, auto
from typing import TypeAlias

from .ref import Ref
from .word import Word


class FormatToken(Enum):
    SENTENCE_START = auto()
    SENTENCE_END = auto()
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()
    LINE_BREAK = auto()


Token: TypeAlias = Word | Ref | FormatToken
