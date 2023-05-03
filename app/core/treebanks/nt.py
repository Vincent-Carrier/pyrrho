from bisect import bisect_left, bisect_right
from itertools import pairwise, takewhile
from pathlib import Path
from typing import Any, NamedTuple, cast

from boltons.iterutils import unique
from dominate.tags import span

from app.core.treebanks.ref import SubDoc

from .conll import ConLL_Treebank
from .ref import NT_Ref, RefRange, SubDoc
from .treebank import Sentence
from .word import Word


class RefIdx(NamedTuple):
    ref: NT_Ref
    sentence_idx: int


class NT_Treebank(ConLL_Treebank):
    _refs: list[RefIdx]

    def __init__(self, f: Path, **kwargs) -> None:
        super().__init__(f, ref_cls=NT_Ref, **kwargs)
        self._refs = unique(
            RefIdx(_get_ref(w), i) for i, s in enumerate(self._conll) for w in s
        )

    def __getitem__(self, ref: SubDoc | str) -> list[Sentence]:
        i, j = 0, 0
        match ref:
            case NT_Ref(b, c, v):
                if v == 0:
                    r = NT_Ref(b, c, 1)
                    i = bisect_left(self._refs, r, key=lambda x: x.ref)
                    return list(
                        takewhile(
                            lambda s: s[-1].subdoc.chapter == c,
                            self.sentences(self._refs[i].sentence_idx),
                        )
                    )
                else:
                    i = bisect_left(self._refs, ref, key=lambda x: x.ref)
                    j = i + 1
            case RefRange(start, end):
                i = bisect_left(self._refs, start, key=lambda x: x.ref)
                j = bisect_right(self._refs, end, key=lambda x: x.ref)
            case str():
                return self[NT_Ref.parse(ref)]
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")
        return list(
            self.sentences(self._refs[i].sentence_idx, self._refs[j].sentence_idx)
        )

    def render_body(self, subdoc: SubDoc | None = None):
        assert type(subdoc) is NT_Ref
        self.render_chapter(subdoc)

    def render_chapter(self, ref: NT_Ref):
        assert ref.verse == 0
        span(ref.chapter, cls="chapter")
        sentences = self[ref]
        for s in sentences:
            self.render_sentence(s)

    @span(cls="sentence")
    def render_sentence(self, sentence: Sentence):
        v = 0
        for w, next in pairwise(sentence):
            verse: int = w.subdoc.verse  # type: ignore
            if verse != v:
                span(verse, cls="verse")
                v = verse
            Word.render(w, next)
        Word.render(sentence[-1])

    def word(self, w: Any) -> Word:
        word = super().word(w)
        word.subdoc = _get_ref(w)
        return word


def _get_ref(w) -> NT_Ref:
    return NT_Ref.parse(list(w.misc["Ref"])[0])
