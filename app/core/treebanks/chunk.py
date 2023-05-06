from abc import ABCMeta, abstractmethod
from typing import Iterable, Protocol

from .ref import Ref, RefLike
from .render import Renderable


class Chunk(metaclass=ABCMeta):
    ref: RefLike

    @abstractmethod
    def __iter__(self) -> Iterable[Renderable]:
        ...

    @abstractmethod
    def __str__(self) -> str:
        ...

class Chapter(Chunk):
    ref: Ref

    def __init__(self, ref: Ref) -> None:
        self.ref = ref

    def __iter__(self) -> Iterable[Renderable]:
        yield from self.ref

    def __str__(self) -> str:
        return str(self.ref)
