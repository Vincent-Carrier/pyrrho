from typing import Any, Generator, Type

import pyconll

from .ref import Ref
from .treebank import Metadata, Sentence, Treebank
from .word import Word


class ConLL_Treebank(Treebank):
    conll: Any

    def __init__(
        self,
        f: str,
        meta: Metadata,
        ref_cls: Type[Ref],
    ) -> None:
        super().__init__(meta, ref_cls=ref_cls)
        self.conll = pyconll.load_from_file(f)
        
    def sentences(self) -> Generator[Sentence, None, None]:
        for sentence in self.conll:
            yield Sentence(
                words=[_word(w) for w in sentence],
                subdoc=Ref(sentence.id),
            )

def _word(w: Any) -> Word:
    kase = w.feats

    return Word(
        id=w.id,
        head=w.head,
        form=w.form,
        lemma=w.lemma,
    )
