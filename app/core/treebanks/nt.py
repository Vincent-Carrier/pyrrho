from bisect import bisect_left, bisect_right
from copy import copy
from pathlib import Path
from typing import Iterator, NamedTuple, Self, cast

from boltons.iterutils import unique

from app.core.treebanks.ref import RefLike

from .conll import ConLL_Treebank
from .ref import NT_Ref, Ref, RefLike, RefRange
from .render import Renderable, Token
from .word import Word


class RefIdx(NamedTuple):
    ref: NT_Ref
    sentence_idx: int


class NT_Treebank(ConLL_Treebank):
    _refs: list[RefIdx]

    def __init__(self, f: Path, **kwargs) -> None:
        super().__init__(f, ref_cls=NT_Ref, **kwargs)
        self._refs = unique(
            RefIdx(_get_ref(w), i) for i, s in enumerate(self.conll) for w in s
        )

    def __getitem__(self, ref: RefLike | str) -> Self:
        i, j = 0, 0
        match ref:
            case str():
                return self[self.parse_reflike(ref)]
            case NT_Ref(b, c, v) as r:
                if r not in self:
                    raise KeyError(f"Cannot find {ref} in {self}")
                if r.is_chapter:
                    r = NT_Ref(b, c, 1)
                    i = bisect_left(self._refs, r, key=lambda x: x.ref)
                    j = bisect_left(self._refs, r, key=lambda x: x.ref) + 2  # TODO
                else:
                    assert r.is_verse
                    i = bisect_left(self._refs, ref, key=lambda x: x.ref)
                    j = i + 1
                tb = copy(self)
                tb.conll = self.conll[i:j]
                tb.ref = r
                return tb
            case RefRange(start, end) as r:
                i = bisect_left(self._refs, start, key=lambda x: x.ref)
                j = bisect_right(self._refs, end, key=lambda x: x.ref)
                tb = copy(self)
                tb.conll = self.conll[i:j]
                tb.ref = r
                return tb
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")

    def __iter__(self) -> Iterator[Renderable]:
        ref = None
        for sentence in self.conll:
            yield Token.SENTENCE_START
            for word in sentence:
                w = self.word(word)
                if w.ref and w.ref != ref:
                    yield cast(Ref, w.ref)
                    ref = w.ref
                yield w
            yield Token.SENTENCE_END

    def word(self, word) -> Word:
        w = super().word(word)
        w.ref = _get_ref(word)
        return w


def _get_ref(w) -> NT_Ref:
    return NT_Ref.parse(next(w.misc["Ref"]))
