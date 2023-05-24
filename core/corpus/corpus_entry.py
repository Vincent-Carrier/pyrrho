from typing import Callable, NamedTuple

from core.treebank import Metadata, Treebank


class CorpusEntry(NamedTuple):
    metadata: Metadata
    new: Callable[[Metadata], Treebank]

    def __call__(self) -> Treebank:
        return self.new(self.metadata)
