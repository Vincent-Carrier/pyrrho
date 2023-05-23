from abc import ABCMeta
from dataclasses import astuple, dataclass
from functools import total_ordering
from typing import Generic, Self, Type, TypeVar, final


@dataclass(order=True, frozen=True, slots=True)
class RefPoint(metaclass=ABCMeta):
    @classmethod
    def parse(cls, ref: str) -> Self:
        return cls(*(int(x) for x in ref.split(".")))

    def __iter__(self):
        yield from astuple(self)

    def __str__(self) -> str:
        return ".".join(str(x) for x in self if x is not None)

    def __contains__(self, ref: object) -> bool:
        if not isinstance(ref, RefPoint):
            raise TypeError(f"Cannot check if {ref} is in {self}")
        for a, b in zip(self, ref):
            if a is None and b is not None:
                return True
            if a != b:
                return False
        return True


T = TypeVar("T", bound=RefPoint)


@final
@dataclass(order=True, frozen=True, slots=True)
class RefRange(Generic[T]):
    start: T
    end: T

    def __post_init__(self) -> None:
        assert self.start <= self.end

    @classmethod
    def parse(cls, ref_cls: Type[T], ref: str) -> Self:
        start, end = ref.split("-")
        return cls(ref_cls.parse(start), ref_cls.parse(end))

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"

    def __contains__(self, obj: object) -> bool:
        match obj:
            case RefRange():
                return self.start <= obj.start <= obj.end <= self.end
            case RefPoint():
                return self.start <= obj <= self.end
            case _:
                raise TypeError(f"Cannot check if {obj} is in {self}")


@total_ordering
@dataclass(frozen=True, slots=True)
class Ref(Generic[T]):
    value: T | RefRange[T]

    @property
    def start(self) -> T:
        return self.value.start if isinstance(self.value, RefRange) else self.value

    @property
    def end(self) -> T:
        return self.value.end if isinstance(self.value, RefRange) else self.value

    def __eq__(self, other: object) -> bool:
        match other:
            case Ref():
                return self.value == other.value
            case RefPoint() | RefRange():
                return self.value == other
        return False

    def __lt__(self, other: Self | T | RefRange[T] | None) -> bool:
        a: RefPoint = self.start
        b: RefPoint
        match other:
            case Ref() as r:
                b = r.start
            case RefPoint() as rp:
                b = rp
            case RefRange() as rr:
                b = rr.start
            case _:
                return False
        return a < b

    def __contains__(self, r: Self) -> bool:
        return self.start <= r.start <= r.end <= self.end

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

    @staticmethod
    def parse(ref_cls: Type[T], string: str) -> "Ref[T]":
        r = RefRange.parse(ref_cls, string) if "-" in string else ref_cls.parse(string)
        return Ref(r)  # type: ignore


@final
@dataclass(order=True, frozen=True, slots=True)
class BCV(RefPoint):
    book: int
    chapter: int | None = None
    verse: int | None = None


@final
@dataclass(order=True, frozen=True, slots=True)
class CV(RefPoint):
    chapter: int
    verse: int | None = None


@final
@dataclass(order=True, frozen=True, slots=True)
class Line(RefPoint):
    line: int
