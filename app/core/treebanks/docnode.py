from typing import Type

from .ref import Ref, SubDoc


class DocNode:
    ref: SubDoc
    children: list[SubDoc]
    ref_cls: Type[Ref]

    def __init__(self, ref: Ref, children: list[SubDoc], ref_cls: Type[Ref]) -> None:
        self.ref = ref
        self.children = children
        self.ref_cls = ref_cls

    def __iter__(self):
        yield self.ref
        yield from self.children
    