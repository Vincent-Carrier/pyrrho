from typing import Callable, NamedTuple, NewType

from core.treebank import Metadata, Treebank

DocId = NewType("DocId", str)


class CorpusEntry(NamedTuple):
    metadata: Metadata
    new: Callable[[Metadata], Treebank]

    def __call__(self) -> Treebank:
        return self.new(self.metadata)
