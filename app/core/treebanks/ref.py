from abc import ABC, abstractmethod
from dataclasses import dataclass


class Ref(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

@dataclass
class BookChapterSection(Ref):
    book: int
    chapter: int
    section: int
    
    def __str__(self) -> str:
        return f"{self.book}.{self.chapter}.{self.section}"
