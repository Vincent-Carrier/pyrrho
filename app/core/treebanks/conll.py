from pathlib import Path
from typing import Any, Generator, Type

import pyconll

from .ref import Ref
from .treebank import Sentence, Treebank
from .word import POS, Case, Word


class ConLL_Treebank(Treebank):
    _conll: Any

    def __init__(
        self,
        f: Path,
        ref_cls: Type[Ref],
        **kwargs,
    ) -> None:
        super().__init__(ref_cls=ref_cls, **kwargs)
        self._conll = pyconll.load_from_file(str(f))

    def sentences(self, start=0, end=-1) -> Generator[Sentence, None, None]:
        for sentence in self._conll[start:end]:
            yield Sentence(
                words=[self.word(w) for w in sentence],
            )

    def word(self, w: Any) -> Word:
        kase = w.feats.get("Case")
        kase = kase and Case.parse_conll(list(kase)[0])
        return Word(
            id=w.id,
            head=w.head,
            form=w.form,
            lemma=w.lemma,
            pos=POS.parse_conll(w.upos),
            case=kase,
        )
