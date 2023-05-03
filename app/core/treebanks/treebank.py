from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Any, Generator, Literal, Type

import dominate
from dominate.tags import link, meta, p, pre, script, span

from .ref import Ref, SubDoc, parse_subdoc
from .word import Word


@dataclass
class Sentence:
    words: list[Word]
    subdoc: SubDoc | None = None

    def __iter__(self):
        return iter(self.words)

    def __getitem__(self, i):
        return self.words[i]

    def __len__(self):
        return len(self.words)
    
    def __str__(self):
        return " ".join(word.form for word in self.words)


Format = Literal["prose", "verse"]
Paragraph = list[Sentence]


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

    def __init__(self, ref_cls: Type[Ref], **kwargs) -> None:
        self.meta = Metadata(**kwargs)
        self.ref_cls = ref_cls

    @abstractmethod
    def __getitem__(self, ref: SubDoc) -> list[Sentence]:
        pass

    @abstractmethod
    def sentences(self) -> Generator[Sentence, None, None]:
        pass

    @abstractmethod
    def render_sentence(self, sentence: Sentence):
        pass

    @abstractmethod
    def render_body(self, subdoc: SubDoc | None = None):
        pass

    def _parse_subdoc(self, subdoc: str) -> SubDoc:
        return parse_subdoc(self.ref_cls, subdoc)

    def _body(self, subdoc: SubDoc | None = None) -> Any:
        with pre(
            cls=f"greek corpus {self.meta.format} syntax", data_urn=self.meta.urn
        ) as body:
            self.render_body(subdoc)

        return body

    def render(self, subdoc: str | None = None) -> str:
        doc = dominate.document(title=self.meta.title)
        with doc.head:  # type: ignore
            meta(name="title", content=self.meta.title)
            meta(name="author", content=self.meta.author)
            link(rel="stylesheet", href="/static/styles.css")
        with doc:
            _subdoc = self._parse_subdoc(subdoc) if subdoc is not None else None
            self._body(_subdoc)
            script(src="https://cdnjs.cloudflare.com/ajax/libs/cash/8.1.5/cash.min.js")
            script(src="https://unpkg.com/@popperjs/core@2")
            script(src="https://unpkg.com/tippy.js@6")
            script(src="/static/reader.js", type="module")

        return doc.render()
