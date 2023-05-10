from copy import copy
from dataclasses import replace
from pathlib import Path
from typing import Any, Iterator, Self, cast, final

from pyrrho import conll

from ..ref import Ref, RefRange
from ..treebank import Renderable, Token
from ..word import Word
from .ref import BCV, RefTree


@final
class GntTreebank(conll.TB[BCV]):
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
        match ref():
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
        

    def __iter__(self) -> Iterator[Renderable]:
        ref: BCV | None = None
        for sentence in self.conll:
            yield Token.SENTENCE_START
            for word in sentence:
                w = self.word(word)
                if self.ref and self.ref < w.ref:
                    raise StopIteration
                if w.ref and w.ref != ref:
                    wref = cast(BCV, w.ref())
                    yield wref
                    ref = wref
                yield w
            yield Token.SENTENCE_END

    def render_next(self) -> Any:
        ...
        # assert self.ref
        # if next := self.ref_tree.next(self.ref):
        #     return a("Next", href=f"/corpus/ag/nt?ref={next}")

    def word(self, word) -> Word:
        w = super().word(word)
        w.ref = get_ref(word)  # type: ignore
        return w


    def get_bcv(self, w) -> BCV:
        [r] = iter(w.misc["Ref"])
        return BCV.parse(r)
