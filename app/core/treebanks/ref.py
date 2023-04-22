from dataclasses import astuple, dataclass


@dataclass(order=True, frozen=True)
class Ref:
    def __iter__(self):
        yield from astuple(self)

    def __str__(self) -> str:
        return ".".join(str(x) for x in self)

    def __contains__(self, ref: object) -> bool:
        if not isinstance(ref, Ref):
            raise TypeError(f"Cannot check if {ref} is in {self}")
        for a, b in zip(self, ref):
            if a is None and b is not None:
                return True
            if a != b:
                return False
        return True

@dataclass
class RefRange:
    start: Ref
    end: Ref

    def __str__(self) -> str:
        return f"{self.start}-{self.end}"

    def __contains__(self, obj: object) -> bool:
        if isinstance(obj, RefRange):
            return self.start <= obj.start <= obj.end <= self.end
        if isinstance(obj, Ref):
            return self.start <= obj <= self.end
        raise TypeError(f"Cannot check if {obj} is in {self}")


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
