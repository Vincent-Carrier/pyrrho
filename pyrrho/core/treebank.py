from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Generic, Iterator, Literal, Self, Type

from .ref import Ref, RefPoint, T
from .token import PUNCTUATION, FormatToken, Token
from .word import Word

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
    def __iter__(self) -> Iterator[Token]:
        ...

    def __str__(self) -> str:
        prev: Word | None = None
        tokens = []
        for t in iter(self):
            match t:
                case Word() as w:
                    if prev and w.form not in PUNCTUATION:
                        tokens.append(" ")
                    tokens.append(w.form)
                    prev = w
                case FormatToken.LINE_BREAK | FormatToken.PARAGRAPH_END:
                    tokens.append("\n")
        return "".join(tokens)
    
    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} title={self.meta.title} ref={self.ref}>"

    def parse_ref(self, ref: str) -> Ref[T]:
        return Ref.parse(self.ref_cls, ref)
