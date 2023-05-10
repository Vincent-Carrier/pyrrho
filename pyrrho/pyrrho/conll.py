from pathlib import Path
from typing import Any, Generic, Iterator, Type

import pyconll

from .constants import LSJ
from .ref import Ref, T
from .treebank import Renderable, Token, Treebank
from .word import POS, Case, Word

lsj = LSJ()


class TB(Generic[T], Treebank[T]):
    conll: Any

    def __init__(
        self,
        f: Path,
        ref_cls: Type[T],
        **kwargs,
    ) -> None:
        super().__init__(ref_cls=ref_cls, **kwargs)
        self.conll = pyconll.load_from_file(str(f))

    def __iter__(self) -> Iterator[Renderable]:
        # TODO: handle subdoc
        for sentence in self.conll:
            yield Token.SENTENCE_START
            yield from (self.word(w) for w in sentence)
            yield Token.SENTENCE_END

    def __contains__(self, ref: Ref[T]) -> bool:
        return True  # TODO

    def word(self, w) -> Word:
        kase = w.feats.get("Case")
        kase = kase and Case.parse_conll(list(kase)[0])
        return Word(
            id=w.id,
            head=w.head,
            form=w.form,
            lemma=w.lemma,
            definition=lsj.get(w.lemma),
            pos=POS.parse_conll(w.upos),
            case=kase,
        )
