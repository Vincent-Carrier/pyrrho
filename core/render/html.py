from abc import ABCMeta
from functools import singledispatch
from typing import Iterable, assert_never, final

import dominate.tags as h
from dominate import document

from core.ref import Ref
from core.token import FT as FT
from core.token import Token
from core.treebank import Treebank
from core.utils import cx
from core.word import POS, Word


class HtmlRenderer(metaclass=ABCMeta):
    tb: Treebank

    def __init__(self, tb: Treebank) -> None:
        self.tb = tb

    def body(self, tokens: Iterable[Token]) -> h.html_tag:
        sentence = h.span(cls="sentence")
        paragraph = h.p()
        container = h.div(cls="treebank syntax")

        for t in tokens:
            match t:
                case Word() as word:
                    sentence += render(word)
                case Ref() as ref:
                    sentence += render(ref)
                case FT.SPACE:
                    sentence += " "
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
                    assert_never(t)
        if len(paragraph):
            container += paragraph
        return container


@singledispatch
def render(obj) -> h.html_tag:
    ...


@render.register(Word)
def _(word: Word) -> h.html_tag:
    return h.span(
        word.form,
        cls=cx(word.case, word.pos == POS.verb and word.pos),
        data_id=str(word.id),
        data_head=str(word.head),
        data_lemma=word.lemma,
        data_flags=word.flags,
        data_def=word.definition,
    )


@render.register(Ref)
def _(ref: Ref) -> h.html_tag:
    if hasattr(ref.value, "render"):
        return ref.value.render()  # type: ignore
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
