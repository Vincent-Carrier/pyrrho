from abc import ABCMeta
from typing import Iterable, final

import dominate.tags as h
from dominate import document

from ..ref import RefPoint
from ..token import PUNCTUATION
from ..token import FormatToken as FT
from ..token import Token
from ..treebank import Treebank
from ..word import Word


class HtmlRenderer(metaclass=ABCMeta):
    def body(self, tokens: Iterable[Token]) -> h.pre:
        prev: Word | None = None
        sentence = h.span(cls="sentence")
        paragraph = h.p()
        container = h.pre(cls="treebank syntax")

        for t in tokens:
            match t:
                case Word() as w:
                    ws = " " if prev and (w.form not in PUNCTUATION) else ""
                    sentence += w.render(ws)
                    prev = w
                case RefPoint() as r:
                    sentence += r.render()
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
                    h.br()
                case None:
                    pass
                case _:
                    raise ValueError(f"Unknown token type: {t!r}")
        if len(paragraph):
            container += paragraph
        return container


@final
class StandaloneRenderer(HtmlRenderer):
    def render(self, tb: Treebank) -> str:
        return self.document(tb).render()

    def document(self, tb) -> document:
        doc = document(title=tb.meta.title)
        pre = self.body(iter(tb))
        with doc.head:  # type: ignore
            h.meta(name="author", content=tb.meta.author)
            h.link(rel="stylesheet", href="/static/styles.css")
        with doc:
            doc.add(pre)
            h.script(
                src="https://cdnjs.cloudflare.com/ajax/libs/cash/8.1.5/cash.min.js"
            )
            h.script(src="https://unpkg.com/@popperjs/core@2")
            h.script(src="https://unpkg.com/tippy.js@6")
            h.script(src="/static/reader.js", type="module")

        return doc
