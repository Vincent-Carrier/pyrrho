from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator, Generic, Literal, Type, TypeVar

from boltons.iterutils import split_iter
from dominate.tags import p, pre, span

from .ref import Ref, RefRange, SubDoc
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

    def paragraphs(self) -> Generator[Paragraph, None, None]:
        yield from split_iter(self.sentences(), lambda a, b: a.subdoc != b.subdoc)

    def render(self, range: RefRange | None = None) -> str:
        with pre(
            cls=f"greek {self.meta.format} syntax", data_urn=self.meta.urn
        ) as html:
            for pg in self.paragraphs():
                with p():
                    span(
                        subdoc := pg[0].subdoc,
                        data_subdoc=subdoc,
                        cls="subdoc",
                    )
                    for s in pg:
                        self.render_sentence(s)

        return html.render()  # type: ignore
