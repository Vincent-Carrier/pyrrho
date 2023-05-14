from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Iterator, Literal, Self, Type

from .constants import PUNCTUATION
from .ref import Ref, RefPoint, T
from .token import FormatToken, Token
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
    chunks: Callable[[Self], Iterator[Self]]

    def __init__(
        self,
        ref_cls: Type[RefPoint],
        chunks: Callable[[Self], Iterator[Self]] | None = None,
        **kwargs,
    ) -> None:
        self.meta = Metadata(**kwargs)
        self.ref_cls = ref_cls
        self.chunks = chunks or (lambda self: iter([self]))

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
        def tokens() -> Iterator[str]:
            prev: Word | None = None
            for t in iter(self):
                match t:
                    case Word() as word:
                        if prev and word.form not in PUNCTUATION:
                            word.left_pad = " "
                        yield str(word)
                        prev = word
                    case FormatToken.LINE_BREAK | FormatToken.PARAGRAPH_END:
                        yield "\n"

        return "".join(tokens())

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} title='{self.meta.title}' ref={self.ref}>"

    def parse_ref(self, ref: str) -> Ref[T]:
        return Ref.parse(self.ref_cls, ref)

