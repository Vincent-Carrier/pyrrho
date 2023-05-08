from typing import Generic, Protocol, TypeVar

from .ref import Ref, RefLike

T = TypeVar("T")

class RefIndex(Generic[T]):
    def next(self, ref: RefLike) -> tuple[Ref, T] | None:
        ...

    def prev(self, ref: RefLike) -> tuple[Ref, T] | None:
        ...

    def __getitem__(self, ref: RefLike) -> T:
        ...
