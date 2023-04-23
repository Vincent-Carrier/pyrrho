from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator, Literal, Self

from boltons.iterutils import split_iter
from dominate.tags import p, pre, span
from word import Word

from app.core.treebanks.ref import Ref, RefRange


@dataclass
class Sentence:
    words: list[Word]
    subdoc: str = ""

    def __iter__(self):
        return iter(self.words)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)


Format = Literal["prose", "verse"]
Paragraph = list[Sentence]


@dataclass
class Metadata:
    title: str = "untitled"
    author: str = "unknown"
    urn: str | None = None
    eng_urn: str | None = None
    start: Ref | None = None
    end: Ref | None = None
    format: Format = "prose"


@dataclass
class Treebank(ABC):
    meta: Metadata

    @property
    def ref_type(self) -> str:
        return type(self.meta.start).__name__

    @abstractmethod
    def __getitem__(self, ref: Ref | RefRange) -> list[Sentence]:
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
