from copy import copy
from dataclasses import replace
from itertools import groupby
from pathlib import Path
from typing import Iterable, Iterator, Self, cast

from .conll import ConLL_Treebank
from .ref import NT_Book, NT_Ref, Ref, RefLike, RefRange, lt_reflike
from .treebank import Renderable, Token
from .word import Word


class RefTree:
    tree: dict[NT_Book, dict[int, list[int]]] = {}

    def __init__(self, refs: Iterable[NT_Ref]) -> None:
        for book, chapters in groupby(refs, key=lambda r: r.book):
            self.tree[book] = {}
            for chapter, verses in groupby(chapters, key=lambda r: r.chapter):
                self.tree[book][chapter] = [r.verse for r in verses]

    def __contains__(self, ref: NT_Ref) -> bool:
        b, c, v = ref
        return b in self.tree and c in self.tree[b] and v in self.tree[b][c]

    def next(self, ref: NT_Ref) -> NT_Ref | None:
        b, c, v = ref
        if ref.is_verse:
            verse = next(iter(self.tree[b][c][v:]), None)
            if verse:
                return replace(ref, verse=verse)
        if ref.is_chapter:
            verses = self.tree[b].get(c + 1)
            return replace(ref, chapter=c + 1) if verses else self.next(NT_Ref(b))
        return None


class NT_Treebank(ConLL_Treebank):
    refs: dict[NT_Ref, int]
    ref_tree: RefTree

    def __init__(self, f: Path, **kwargs) -> None:
        super().__init__(f, ref_cls=NT_Ref, **kwargs)
        self.refs = {get_ref(w): i for i, s in enumerate(self.conll) for w in s}
        self.ref_tree = RefTree(self.refs.keys())

    def __getitem__(self, ref: RefLike | str) -> Self:
        i, j = 0, 0
        match ref:
            case str():
                return self[self.parse_reflike(ref)]
            case NT_Ref() as r:
                if r.is_book:
                    raise NotImplementedError
                if r.is_chapter:
                    start = replace(r, verse=1)
                rr = RefRange(r, self.ref_tree.next(r) or r)
                return self[rr]
            case RefRange(start, end) as rr:
                i = self.refs[start]
                j = self.refs[end]
                tb = copy(self)
                tb.conll = self.conll[i:j]
                tb.ref = rr
                return tb
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")

    def __iter__(self) -> Iterator[Renderable]:
        ref: RefLike | None = None
        for sentence in self.conll:
            yield Token.SENTENCE_START
            for word in sentence:
                w = self.word(word)
                if self.ref and lt_reflike(self.ref, w.ref):
                    break
                if w.ref and w.ref != ref:
                    yield cast(Ref, w.ref)
                    ref = w.ref
                yield w
            yield Token.SENTENCE_END

    def word(self, word) -> Word:
        w = super().word(word)
        w.ref = get_ref(word)
        return w


def get_ref(w) -> NT_Ref:
    [r] = iter(w.misc["Ref"])
    return NT_Ref.parse(r)
