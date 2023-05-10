from dataclasses import dataclass, replace
from itertools import groupby
from typing import Iterable, Self, final

from dominate.tags import span
from ordered_enum import OrderedEnum  # type: ignore

from ..ref import RefPoint


class Book(OrderedEnum):
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


@final
@dataclass(order=True, frozen=True, slots=True)
class BCV(RefPoint):
    book: Book
    chapter: int = 0
    verse: int = 0

    def __str__(self):
        if self.is_chapter:
            return f"{self.book.value}_{self.chapter}"
        else:
            return f"{self.book.value}_{self.chapter}.{self.verse}"

    @property
    def is_book(self) -> bool:
        return self.chapter == 0 and self.verse == 0

    @property
    def is_chapter(self) -> bool:
        return self.chapter > 0 and self.verse == 0

    @property
    def is_verse(self) -> bool:
        assert self.chapter > 0
        return self.verse != 0

    def render(self) -> span:
        if self.is_chapter:
            return span(self.chapter, cls="chapter")
        elif self.is_verse:
            return span(self.verse, cls="verse")
        else:
            raise ValueError("cannot render {self}")

    @classmethod
    def parse(cls, ref: str) -> Self:
        b, cv = ref.split("_")
        if "." in cv:
            c, v = cv.split(".")
            return cls(Book(b), int(c), int(v))
        else:
            return cls(Book(b), int(cv), 0)


class RefTree:
    tree: dict[Book, dict[int, list[int]]] = {}

    def __init__(self, refs: Iterable[BCV]) -> None:
        for book, chapters in groupby(refs, key=lambda r: r.book):
            self.tree[book] = {}
            for chapter, verses in groupby(chapters, key=lambda r: r.chapter):
                self.tree[book][chapter] = [r.verse for r in verses]

    def __getitem__(self, ref: BCV) -> list[int]:
        b, c, _ = ref
        assert ref.is_chapter
        return self.tree[b][c]
    
    def __contains__(self, ref: BCV) -> bool:
        b, c, v = ref
        return b in self.tree and c in self.tree[b] and v in self.tree[b][c]

    def next(self, ref: BCV) -> BCV | None:
        b, c, v = ref
        if ref.is_verse:
            verse = next(iter(self.tree[b][c][v:]), None)
            if verse:
                return replace(ref, verse=verse)
        if ref.is_chapter:
            verses = self.tree[b].get(c + 1)
            return replace(ref, chapter=c + 1) if verses else self.next(BCV(b))
        return None
