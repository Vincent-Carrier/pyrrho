from abc import ABC, abstractmethod
from typing import Generator, Literal

from boltons.iterutils import split_iter
from dominate.tags import *  # type: ignore
from word import *

from app.core.treebanks.ref import Ref


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


@dataclass
class Treebank(ABC):
    format: Format
    meta: Metadata

    @property
    def ref_type(self) -> str:
        return type(self.meta.start).__name__

    @abstractmethod
    def sentences(self) -> Generator[Sentence, None, None]:
        pass

    @abstractmethod
    def sentence(self, sentence: Sentence):
        pass

    def paragraphs(self) -> Generator[Paragraph, None, None]:
        yield from split_iter(
            self.sentences(), lambda a, b: a.subdoc != b.subdoc
        )

    def render(self) -> str:
        with pre(cls=f"greek {self.format} syntax", data_urn=self.meta.urn) as html:
            for pg in self.paragraphs():
                with p():
                    span(
                        subdoc := pg[0].subdoc,
                        data_subdoc=subdoc,
                        cls="subdoc",
                    )
                    for s in pg:
                        self.sentence(s)

        return html.render()



