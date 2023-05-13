from abc import ABC
from functools import singledispatch
from typing import Iterable, final

import dominate.tags as h
from dominate import document

from ..ref import RefPoint
from ..token import PUNCTUATION
from ..token import FormatToken as FT
from ..token import Token
from ..treebank import Treebank
from ..utils import cx
from ..word import POS, Word


class HtmlRenderer(ABC):
    tb: Treebank

    def __init__(self, tb: Treebank) -> None:
        self.tb = tb

    def body(self, tokens: Iterable[Token]) -> h.html_tag:
        prev: Word | None = None
        sentence = h.span(cls="sentence")
        paragraph = h.p()
        container = h.pre(cls="treebank syntax")

        for t in tokens:
            match t:
                case Word() as word:
                    if prev and (word.form not in PUNCTUATION):
                        word.left_pad = " "
                    sentence += render(word)
                    prev = word
                case RefPoint() as rp:
                    sentence += render(rp)
                case FT.SENTENCE_START:
                    sentence = h.span(cls="sentence")
                case FT.SENTENCE_END:
                    if len(sentence):
                        paragraph += sentence
                case FT.PARAGRAPH_START:
                    paragraph = h.p()
                case FT.PARAGRAPH_END:
                    if len(paragraph):
                        container += paragraph
                case FT.LINE_BREAK:
                    sentence += h.br()
                case None:
                    pass
                case _:
                    raise ValueError(f"Unknown token type: {t!r}")
        if len(paragraph):
            container += paragraph
        return container


@singledispatch
def render(obj) -> h.html_tag:
    ...


@render.register(Word)
def _(word: Word) -> h.html_tag:
    return h.span(
        f"{word.left_pad}{word.form}",
        cls=cx(word.case, word.pos == POS.verb and word.pos),
        data_id=str(word.id),
        data_head=str(word.head),
        data_lemma=word.lemma,
        data_flags=word.flags,
        data_def=word.definition,
    )


@render.register(RefPoint)
def _(ref: RefPoint) -> h.html_tag:
    return h.span(str(ref), cls="ref")


@final
class StandaloneRenderer(HtmlRenderer):
    def __str__(self) -> str:
        return self.document(self.tb).render()

    def document(self, tb) -> document:
        doc = document(title=tb.meta.title)
        pre = self.body(iter(tb))
        text = h.div(pre, cls=f"{tb.meta.format}-format")
        with doc.head:  # type: ignore
            h.meta(name="author", content=tb.meta.author)
            h.link(rel="stylesheet", href="/static/styles.css")
        with doc:
            doc.add(text)
            h.script(
                src="https://cdnjs.cloudflare.com/ajax/libs/cash/8.1.5/cash.min.js"
            )
            h.script(src="https://unpkg.com/@popperjs/core@2")
            h.script(src="https://unpkg.com/tippy.js@6")
            h.script(src="/static/reader.js", type="module")

        return doc
