from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Generic, Iterator, Literal, Self, Type, TypeAlias, cast

import dominate
from dominate.tags import a, br, link, meta, p, pre, script, span

from .ref import Ref, RefPoint, T
from .word import Word


class Token(Enum):
    SENTENCE_START = auto()
    SENTENCE_END = auto()
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()
    LINE_BREAK = auto()


Renderable: TypeAlias = Word | RefPoint | Token
Format = Literal["prose", "verse"]


@dataclass(slots=True)
class Metadata:
    title: str = "<untitled>"
    author: str = "<unknown>"
    urn: str | bytes | None = None
    eng_urn: str | bytes | None = None
    format: Format = "prose"


class Treebank(Generic[T], metaclass=ABCMeta):
    meta: Metadata
    ref_cls: Type[RefPoint]
    ref: Ref | None = None

    def __init__(self, ref_cls: Type[RefPoint], **kwargs) -> None:
        self.meta = Metadata(**kwargs)
        self.ref_cls = ref_cls

    @abstractmethod
    def __getitem__(self, ref: Ref | str) -> Self:
        ...

    @abstractmethod
    def __contains__(self, ref: Ref) -> bool:
        ...

    @abstractmethod
    def __iter__(self) -> Iterator[Renderable]:
        ...

    def __str__(self) -> str:
        prev: Word | None = None
        tokens = []
        for t in iter(self):
            match t:
                case Word() as w:
                    if prev and prev.form not in [".", ",", ";", ":", "·", "]", ")"]:
                        tokens.append(" ")
                    tokens.append(w.form)
                    prev = w
                case Token.LINE_BREAK | Token.PARAGRAPH_END:
                    tokens.append("\n")
                case _:
                    ...
        return "".join(tokens)

    def html(self) -> str:
        doc = dominate.document(title=self.meta.title)
        body = self.render()
        with doc.head:  # type: ignore
            meta(name="author", content=self.meta.author)
            link(rel="stylesheet", href="/static/styles.css")
        with doc:
            doc.add(body)
            self.render_next()
            script(src="https://cdnjs.cloudflare.com/ajax/libs/cash/8.1.5/cash.min.js")
            script(src="https://unpkg.com/@popperjs/core@2")
            script(src="https://unpkg.com/tippy.js@6")
            script(src="/static/reader.js", type="module")

        return doc.render()

    def render(self) -> pre:
        prev: Word | None = None
        sentence = span(cls="sentence")
        paragraph = p()
        container = pre(cls=f"greek corpus {self.meta.format} syntax")

        for t in iter(self):
            match t:
                case Word() as w:
                    ws = " " if prev and prev.form not in PUNCTUATION else ""
                    sentence += w.render(ws)
                    prev = w
                case RefPoint() as r:
                    sentence += r.render()
                case Token.SENTENCE_START:
                    sentence = span(cls="sentence")
                case Token.SENTENCE_END:
                    if len(sentence):
                        paragraph += sentence
                case Token.PARAGRAPH_START:
                    paragraph = p()
                case Token.PARAGRAPH_END:
                    if len(paragraph):
                        container += paragraph
                case Token.LINE_BREAK:
                    br()
                case _:
                    raise ValueError(f"Unknown token type: {t!r}")
        if len(paragraph):
            container += paragraph
        return container

    def render_next(self) -> Any:
        ...

    def parse_ref(self, ref: str) -> Ref[T]:
        return Ref.parse(self.ref_cls, ref)


PUNCTUATION = [".", ",", ";", ":", "·", "]", ")"]
