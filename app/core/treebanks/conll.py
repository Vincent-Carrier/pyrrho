import shelve
from pathlib import Path
from typing import Any, Iterator, Type

import pyconll

from .ref import Ref
from .render import Renderable, Token
from .treebank import Treebank
from .word import POS, Case, Word

lsj = shelve.open("data/ag/lsj")

class ConLL_Treebank(Treebank):
    conll: Any

    def __init__(
        self,
        f: Path,
        ref_cls: Type[Ref],
        **kwargs,
    ) -> None:
        super().__init__(ref_cls=ref_cls, **kwargs)
        self.conll = pyconll.load_from_file(str(f))

    def tokens(self) -> Iterator[Renderable]:
        # TODO: handle subdoc
        for sentence in self.conll:
            yield Token.SENTENCE_START
            yield from (self.word(w) for w in sentence)
            yield Token.SENTENCE_END

    def word(self, w: Any) -> Word:
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
