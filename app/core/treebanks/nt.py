from bisect import bisect_left, bisect_right
from pathlib import Path
from typing import Any

from boltons.iterutils import unique

from .conll import ConLL_Treebank
from .ref import NT_Ref, Ref, RefRange, SubDoc
from .treebank import Sentence


class NT_Treebank(ConLL_Treebank):
    _refs: list[NT_Ref]

    def __init__(self, f: Path, **kwargs) -> None:
        super().__init__(f, ref_cls=NT_Ref, **kwargs)
        self._refs= unique((_get_ref(w), i) for i, s in enumerate(self._conll) for w in s)

    def __getitem__(self, ref: SubDoc | str) -> list[Any]:
        i, j = 0, 0
        match ref:
            case Ref():
                i = bisect_left(self._refs, ref, key=lambda x: x[0]) # type: ignore
                j = i
            case RefRange(start, end):
                i = bisect_left(self._refs, start, key=lambda x: x[0]) # type: ignore
                j = bisect_right(self._refs, end, key=lambda x: x[0]) # type: ignore
            case str():
                return self[NT_Ref.parse(ref)]
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")
        return self._conll[i:j]
    
    


def _get_ref(w) -> NT_Ref:
    return NT_Ref.parse(list(w.misc['Ref'])[0])
