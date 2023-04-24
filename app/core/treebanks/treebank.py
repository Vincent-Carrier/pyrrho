from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import takewhile
from typing import Any, Generator, Literal, Type

import dominate
from dominate.tags import div, meta, p, span

from .ref import Ref, SubDoc
from .word import Word


@dataclass
class Sentence:
    words: list[Word]
    subdoc: SubDoc  # | None = None

    def __iter__(self):
        return iter(self.words)

    def __getitem__(self, i):
        return self.words[i]

    def __len__(self):
        return len(self.words)


Format = Literal["prose", "verse"]
Paragraph = list[Sentence]


@dataclass(slots=True)
class Metadata:
    title: str = "<untitled>"
    author: str = "<unknown>"
    urn: str | bytes | None = None
    eng_urn: str | bytes | None = None
    format: Format = "prose"


@dataclass
class Treebank(ABC):
    meta: Metadata
    ref_cls: Type[Ref]
    start: Ref | None = None
    end: Ref | None = None

    @abstractmethod
    def __getitem__(self, ref: SubDoc) -> list[Sentence]:
        pass

    @abstractmethod
    def sentences(self) -> Generator[Sentence, None, None]:
        pass

    @abstractmethod
    def render_sentence(self, sentence: Sentence):
        pass

    def paragraphs(
        self, sentences: list[Sentence] | None
    ) -> Generator[Paragraph, None, None]:
        sentences_iter = self.sentences() if sentences is None else iter(sentences)
        yield list(takewhile(lambda s: s.subdoc != self.end, sentences_iter))

    def _body(self, subdoc: SubDoc | None = None) -> Any:
        with div(
            cls=f"greek corpus {self.meta.format} syntax", data_urn=self.meta.urn
        ) as body:
            for pg in (
                self.paragraphs(None)
                if subdoc is None
                else self.paragraphs(self[subdoc])
            ):
                with p():
                    span(
                        ref := str(pg[0].subdoc),
                        data_subdoc=ref,
                        cls="subdoc",
                    )
                    for s in pg:
                        self.render_sentence(s)

        return body
    
    def render(self, subdoc: SubDoc | None = None) -> str:
        doc = dominate.document(title=self.meta.title)
        with doc.head: # type: ignore
            meta(name="title", content=self.meta.title)
            meta(name="author", content=self.meta.author)
        with doc:
            self._body(subdoc)

        return doc.render()

