from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import Callable, Generic, Iterator, Literal, Self, Type

from core.ref import Ref, T
from core.token import FT, Token
from core.word import Word

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
    ref_cls: Type[T]
    ref: Ref | None = None
    chunks: Callable[[Self], Iterator[Self]]

    def __init__(
        self,
        ref_cls: Type[T],
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
        def render(t: Token) -> str:
            match t:
                case Word() as word:
                    return str(word)
                case FT.SPACE:
                    return " "
                case FT.LINE_BREAK | FT.PARAGRAPH_END:
                    return "\n"
                case _:
                    return ""

        return "".join(render(t) for t in iter(self))

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} title='{self.meta.title}' ref={self.ref}>"

    def parse_ref(self, ref: str) -> Ref[T]:
        return Ref.parse(self.ref_cls, ref)

