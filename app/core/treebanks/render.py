from enum import Enum
from itertools import takewhile
from typing import Iterable

from dominate.tags import br, span
from dominate.util import text

from .ref import Ref
from .word import Word


class Token(Enum):
    SENTENCE_START = "SENTENCE_START"
    SENTENCE_END = "SENTENCE_END"
    PARAGRAPH_START = "PARAGRAPH_START"
    PARAGRAPH_END = "PARAGRAPH_END"
    LINE_BREAK = "LINE_BREAK"


Renderable = Word | Ref | Token


def render(tokens: Iterable[Renderable]) -> Iterable[Renderable]:
    prev = None
    for t in tokens:
        match t:
            case Word() as w:
                if prev and prev.form not in [".", ",", ";", ":", "·", "]", ")"]:
                    text(" ")
                w.render()
                prev = w
            case Ref() as r:
                r.render()
            case Token.SENTENCE_START:
                with span(cls="sentence"):
                    takewhile(lambda t: t != "SENTENCE_END", render(tokens))
            case "SENTENCE_END":
                pass
            case Token.PARAGRAPH_START:
                with span(cls="paragraph"):
                    takewhile(lambda t: t != "PARAGRAPH_END", render(tokens))
            case Token.PARAGRAPH_END:
                pass
            case Token.LINE_BREAK:
                br()
            case _:
                raise ValueError(f"Unknown token type: {t!r}")
        yield t
