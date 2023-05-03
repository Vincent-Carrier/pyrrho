from abc import ABC
from dataclasses import astuple, dataclass
from itertools import takewhile
from typing import Self, Type

from ordered_enum import OrderedEnum  # type: ignore


@dataclass(order=True, frozen=True)
class Ref(ABC):
    def __iter__(self):
        yield from astuple(self)

    def __str__(self) -> str:
        return ".".join(str(x) for x in self if x is not None)

    @classmethod
    def parse(cls, ref: str) -> Self:
        return cls(*(int(x) for x in ref.split(".")))

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
    def parse(cls, ref_cls: Type[Ref], ref: str) -> Self:
        start, end = ref.split("-")
        return cls(ref_cls.parse(start), ref_cls.parse(end))

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


def parse_subdoc(ref_cls, subdoc: str) -> SubDoc:
    return RefRange.parse(ref_cls, subdoc) if "-" in subdoc else ref_cls.parse(subdoc)


@dataclass(order=True, frozen=True, slots=True)
class BCV(Ref):
    book: int
    chapter: int | None = None
    verse: int | None = None


@dataclass(order=True, frozen=True, slots=True)
class CV(Ref):
    chapter: int
    verse: int | None = None


@dataclass(order=True, frozen=True, slots=True)
class Line(Ref):
    line: int


class NT_Book(OrderedEnum):
    MATT = "MATT"
    MARK = "MARK"
    LUKE = "LUKE"
    JOHN = "JOHN"
    ACTS = "ACTS"
    ROM = "ROM"
    COR1 = "1COR"
    COR2 = "2COR"
    GAL = "GAL"
    EPH = "EPH"
    PHIL = "PHIL"
    COL = "COL"
    THESS1 = "1THESS"
    THESS2 = "2THESS"
    TIM1 = "1TIM"
    TIM2 = "2TIM"
    TIT = "TIT"
    PHILEM = "PHILEM"
    HEB = "HEB"
    JAS = "JAS"
    PET1 = "1PET"
    JOHN3 = "3JOHN"
    JUDE = "JUDE"
    REV = "REV"


@dataclass(order=True, frozen=True, slots=True)
class NT_Ref(Ref):
    book: NT_Book
    chapter: int
    verse: int # we use 0 to indicate a chapter ref, so that we get implicit ordering

    def __str__(self):
        if self.verse != 0:
            return f"{self.book.value}_{self.chapter}.{self.verse}"
        else:
            return f"{self.book.value}_{self.chapter}"


    @classmethod
    def parse(cls, ref: str) -> Self:
        b, cv = ref.split("_")
        if "." in cv:
            c, v = cv.split(".")
            return cls(NT_Book(b), int(c), int(v))
        else:
            return cls(NT_Book(b), int(cv), 0)

    # TODO __contains__
