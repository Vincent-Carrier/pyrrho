from dataclasses import astuple, dataclass
from functools import total_ordering
from typing import NamedTuple


@dataclass(order=True)
class Ref:
    def __iter__(self):
        yield from astuple(self)

    def __str__(self) -> str:
        return ".".join(str(x) for x in self)


@dataclass
class Range:
    start: Ref
    end: Ref

    def __contains__(self, ref: object) -> bool:
        if not isinstance(ref, Ref):
            raise TypeError(f"Cannot check if {ref} is in {self}")
        return self.start <= ref <= self.end


@dataclass(order=True)
class BCV(Ref):
    book: int
    chapter: int
    verse: int | None


@dataclass(order=True)
class CV(Ref):
    chapter: int
    verse: int


@dataclass(order=True)
class Line(Ref):
    line: int
