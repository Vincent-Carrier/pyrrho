from pathlib import Path
from typing import Any, Generic, Iterator, Type

import pyconll
from pyconll.unit.conll import Conll
from pyconll.unit.token import Token as ConllToken

from .constants import LSJ
from .ref import Ref, T
from .token import FT
from .treebank import Token, Treebank
from .word import POS, Case, Word

lsj = LSJ()


class TB(Generic[T], Treebank[T]):
    conll: Conll

    def __init__(
        self,
        f: Path,
        ref_cls: Type[T],
        **kwargs,
    ) -> None:
        super().__init__(ref_cls=ref_cls, **kwargs)
        self.conll = pyconll.load_from_file(str(f))

    def __iter__(self) -> Iterator[Token]:
        for sentence in self.conll:
            yield FT.SENTENCE_START
            for w in sentence:
                yield self.word(w)
                yield FT.SPACE
            yield FT.SENTENCE_END

    def __contains__(self, ref: Ref[T]) -> bool:
        return True  # TODO

    def word(self, t: ConllToken) -> Word:
        return Word(
            id=int(t.id),
            head=int(t.head) if t.head else None,
            form=t.form or "",
            lemma=t.lemma,
            definition=lsj.get(t.lemma) if t.lemma else None,
            pos=POS.parse_conll(t.upos),
            case=(c := t.feats and t.feats.get("Case")) and Case.parse_conll(next(iter(c))),  # type: ignore
        )
