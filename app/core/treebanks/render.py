from enum import Enum

from .ref import Ref
from .word import Word


class Token(Enum):
    SENTENCE_START = "SENTENCE_START"
    SENTENCE_END = "SENTENCE_END"
    PARAGRAPH_START = "PARAGRAPH_START"
    PARAGRAPH_END = "PARAGRAPH_END"
    LINE_BREAK = "LINE_BREAK"


Renderable = Word | Ref | Token
