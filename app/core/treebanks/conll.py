from pathlib import Path
from typing import Any, Generator, Type

import pyconll

from .ref import Ref, parse_subdoc
from .treebank import Metadata, Sentence, Treebank
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
        
    
    def sentences(self) -> Generator[Sentence, None, None]:
        for sentence in self._conll:
            yield Sentence(
                words=[_word(w) for w in sentence],
                subdoc=parse_subdoc(self.ref_cls, sentence.id),
            )


    def render_sentence(self, sentence: Sentence):
        pass

def _word(w: Any) -> Word:
    return Word(
        id=w.id,
        head=w.head,
        form=w.form,
        lemma=w.lemma,
        pos=POS.parse_conll(w.upos),
        case=Case.parse_conll(w.feats.get("Case"))
    )
