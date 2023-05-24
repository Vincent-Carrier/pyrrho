from copy import copy
from dataclasses import replace
from pathlib import Path
from typing import Iterator, Self, cast, final

from pyconll.unit.token import Token as ConllToken

from core.conll import ConllTB
from core.nt.ref import BCV, RefTree
from core.ref import Ref, RefRange
from core.token import FT
from core.treebank import Token
from core.word import Word


@final
class GntTB(ConllTB[BCV]):
    refs: dict[BCV, int]
    ref_tree: RefTree

    def __init__(self, f: Path, **kwargs) -> None:
        super().__init__(f, ref_cls=BCV, **kwargs)
        self.refs = {self.get_bcv(w): i for i, s in enumerate(self.conll) for w in s}
        self.ref_tree = RefTree(self.refs.keys())

    def __getitem__(self, ref: Ref[BCV] | str) -> Self:
        i, j = 0, 0
        r: RefRange[BCV]
        if isinstance(ref, str):
            return self[self.parse_ref(ref)]
        match ref.value:
            case BCV() as bcv:
                if bcv.is_book:
                    raise NotImplementedError
                elif bcv.is_chapter:
                    start = replace(bcv, verse=1)
                    end = replace(bcv, verse=self.ref_tree[bcv][-1])
                    r = RefRange(start, end)
                else:
                    r = RefRange(bcv, self.ref_tree.next(bcv) or bcv)
            case RefRange() as rr:
                r = rr
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")
        i = self.refs[r.start]
        j = self.refs[r.end]
        tb = copy(self)
        tb.conll = self.conll[i:j]
        tb.ref = Ref(r)
        return tb

    def __iter__(self) -> Iterator[Token]:
        ref: BCV | None = None
        for sentence in self.conll:
            yield FT.SENTENCE_START
            for word in sentence:
                w = self.word(word)
                yield FT.SPACE
                if w.ref and self.ref and w.ref not in self.ref:
                    return
                if w.ref and w.ref != ref:
                    yield w.ref
                    ref = cast(BCV, w.ref.value)
                yield w
            yield FT.SENTENCE_END

    def word(self, token: ConllToken) -> Word:
        return replace(super().word(token), ref=Ref(self.get_bcv(token)))

    def get_bcv(self, token: ConllToken) -> BCV:
        [r] = iter(token.misc["Ref"])  # type: ignore
        return BCV.parse(r)
