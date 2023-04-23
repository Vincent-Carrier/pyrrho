from abc import ABC
from dataclasses import astuple, dataclass
from typing import Self


@dataclass(order=True, frozen=True)
class Ref(ABC):
    def __iter__(self):
        yield from astuple(self)

    def __str__(self) -> str:
        return ".".join(str(x) for x in self if x is not None)

    @classmethod
    def parse(cls, ref: str) -> Self:
        return cls(*[int(x) for x in ref.split(".")])

    def __contains__(self, ref: object) -> bool:
        if not isinstance(ref, Ref):
            raise TypeError(f"Cannot check if {ref} is in {self}")
        for a, b in zip(self, ref):
            if a is None and b is not None:
                return True
            if a != b:
                return False
        return True


@dataclass(order=True, frozen=True)
class RefRange:
    start: Ref
    end: Ref

    @classmethod
    def parse(cls, ref: str) -> Self:
        start, end = ref.split("-")
        return cls(Ref.parse(start), Ref.parse(end))

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"

    def __contains__(self, obj: object) -> bool:
        match obj:
            case RefRange():
                return self.start <= obj.start <= obj.end <= self.end
            case Ref():
                return self.start <= obj <= self.end
            case _:
                raise TypeError(f"Cannot check if {obj} is in {self}")


SubDoc = Ref | RefRange


@dataclass(order=True, frozen=True, slots=True)
class BCV(Ref):
    book: int
    chapter: int
    verse: int | None


@dataclass(order=True, frozen=True, slots=True)
class CV(Ref):
    chapter: int
    verse: int


@dataclass(order=True, frozen=True, slots=True)
class Line(Ref):
    line: int
