from enum import Enum, auto
from typing import TypeAlias

from core.ref import Ref
from core.word import Word


class FT(Enum):  # Formatting Token
    SPACE = auto()
    SENTENCE_START = auto()
    SENTENCE_END = auto()
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()
    LINE_BREAK = auto()


Token: TypeAlias = Word | Ref | FT
