from dataclasses import dataclass
from typing import NamedTuple


class Ref(NamedTuple):
    def __str__(self) -> str:
        return ".".join(self._asdict().values())

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError()

    def __lt__(self, other: object) -> bool:
        raise NotImplementedError()

    def __contains__(self, other: object) -> bool:
        raise NotImplementedError()


class Range(NamedTuple):
    start: Ref
    end: Ref


class BookChapterSection(Ref):
    book: int
    chapter: int
    section: int

    def __str__(self) -> str:
        return f"{self.book}.{self.chapter}.{self.section}"


@dataclass
class ChapterVerse(Ref):
    chapter: int
    verse: int
