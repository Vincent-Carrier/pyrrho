from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Iterator, Literal, Self, Type

import dominate
from dominate.tags import link, meta, pre, script

from .ref import Ref, RefLike, parse_reflike
from .render import Renderable, render

Format = Literal["prose", "verse"]


@dataclass(slots=True)
class Metadata:
    title: str = "<untitled>"
    author: str = "<unknown>"
    urn: str | bytes | None = None
    eng_urn: str | bytes | None = None
    format: Format = "prose"


class Treebank(metaclass=ABCMeta):
    meta: Metadata
    ref_cls: Type[Ref]
    ref: RefLike | None = None

    def __init__(self, ref_cls: Type[Ref], **kwargs) -> None:
        self.meta = Metadata(**kwargs)
        self.ref_cls = ref_cls

    @abstractmethod
    def __getitem__(self, ref: RefLike | str) -> Self:
        ...

    @abstractmethod
    def __contains__(self, ref: RefLike | str) -> bool:
        ...

    @abstractmethod
    def __iter__(self, ref) -> Iterator[Renderable]:
        ...

    def render_body(self):
        render(iter(self))  # type: ignore

    def parse_reflike(self, ref: str) -> RefLike:
        return parse_reflike(self.ref_cls, ref)

    def render(self) -> str:
        doc = dominate.document(title=self.meta.title)
        with doc.head:  # type: ignore
            meta(name="title", content=self.meta.title)
            meta(name="author", content=self.meta.author)
            link(rel="stylesheet", href="/static/styles.css")
        with doc:
            with pre(cls=f"greek corpus {self.meta.format} syntax"):
                self.render_body()
            script(src="https://cdnjs.cloudflare.com/ajax/libs/cash/8.1.5/cash.min.js")
            script(src="https://unpkg.com/@popperjs/core@2")
            script(src="https://unpkg.com/tippy.js@6")
            script(src="/static/reader.js", type="module")

        return doc.render()
