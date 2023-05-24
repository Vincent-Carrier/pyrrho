from functools import singledispatch
from typing import assert_never

from rich.console import Console
from rich.style import Style

from core.ref import Ref
from core.token import FT as FT
from core.treebank import Treebank
from core.word import POS, Case, Word

console = Console()


class TerminalRenderer:
    tb: Treebank

    def __init__(self, tb: Treebank) -> None:
        self.tb = tb

    def render(self) -> None:
        for t in iter(self.tb):
            match t:
                case Word() as word:
                    render(word)
                case Ref() as ref:
                    render(ref)
                case FT.SPACE:
                    console.print(" ", end="")
                case FT.PARAGRAPH_END | FT.LINE_BREAK:
                    console.print()
                case FT.SENTENCE_START | FT.SENTENCE_END | FT.PARAGRAPH_START | None:
                    pass
                case _:
                    assert_never(t)


@singledispatch
def render(obj) -> None:
    ...


@render.register(Word)
def _(word: Word) -> None:
    colors = {
        Case.nominative: "green",
        Case.accusative: "cyan",
        Case.genitive: "magenta",
        Case.dative: "red",
        Case.vocative: "yellow",
        None: None,
    }
    style = Style(color=colors.get(word.case), bold=(word.pos == POS.verb))
    console.print(word.form, end="", style=style)


@render.register(Ref)
def _(ref: Ref) -> None:
    console.print("— ", end="", style="white")
