import re
import shelve
from copy import copy
from itertools import dropwhile, takewhile
from pathlib import Path
from typing import Iterator, Self, Type

from lxml import etree

from app.core.treebanks.ref import RefLike
from app.core.treebanks.render import Renderable

from ..utils import at
from .ref import Ref, RefRange
from .render import Renderable, Token
from .treebank import Treebank
from .word import POS, Case, Word


class PerseusTreebank(Treebank):
    body: etree._Element
    gorman: bool
    _reflikes: list[RefLike] = []

    def __init__(
        self,
        f: Path,
        ref_cls: Type[Ref],
        gorman: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(ref_cls=ref_cls, **kwargs)
        self.gorman = gorman

        if not self.ref:
            tree = etree.parse(f)
            root = tree.getroot()
            if gorman:
                self.body = root
            else:
                self.body = root.find(".//body")  # type: ignore
            assert self.body is not None

            self.meta.urn = root.attrib.get("cts")
            if self.meta.urn is None:
                self.meta.urn = self.body.find(".//sentence").attrib.get("document_id")  # type: ignore
            if self.meta.urn:
                self.meta.urn = self.normalize_urn(self.meta.urn)

            self._reflikes = [
                self.parse_reflike(reflike)
                for sentence in self.body.findall(".//sentence")
                if (rl := sentence.attrib.get("subdoc")) is not None
                and (reflike := str(rl)) != ""
            ]

    def __getitem__(self, ref: RefLike | str) -> Self:
        match ref:
            case str():
                return self[self.parse_reflike(ref)]
            case RefRange() | Ref() as r:
                tb = copy(self)
                tb.ref = r
                if ref not in self:
                    raise KeyError(f"Cannot find {ref} in {self}")
                el = self.body.find(f".//sentence[@subdoc='{ref}']")
                return tb
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")

    def sentences(self) -> Iterator[etree._Element]:
        yield from self.body.findall(".//sentence")

    def tokens(self) -> Iterator[Renderable]:
        # TODO: yield paragraph tokens
        for sentence in self.sentences():
            yield Token.SENTENCE_START
            yield from (self.word(el.attrib) for el in sentence)  # type: ignore
            yield Token.SENTENCE_END


    def normalize_urn(self, urn: str | bytes) -> str:
        return re.search(r"^(urn:cts:greekLit:tlg\d{4}.tlg\d{3}).*", str(urn)).group(1)  # type: ignore

    # def sentences(self) -> Iterator[Sentence]:
    #     yield from (self.sentence(el) for el in self.body.findall(".//sentence"))  # type: ignore

    # def sentence(self, el: Element) -> Sentence:
    #     words: list[Word] = [
    #         w for token in el if (w := _word(token.attrib)) is not None
    #     ]
    #     return Sentence(words, self._parse_subdoc(el.attrib["subdoc"]))

    def _word(self, attr: dict) -> Word | None:
        if attr.get("insertion_id") is not None:  # TODO
            return None

        tags = attr.get("postag")
        pos = POS.parse_agldt(at(tags, 0))
        case = Case.parse_agldt(at(tags, 7))

        lemma = attr.get("lemma")
        if lemma:
            lemma = re.sub(r"\d+$", "", lemma)

        def parse_int(s: str | None) -> int | None:
            if s is None:
                return None
            return int(s) if s else None

        return Word(
            id=parse_int(attr.get("id")),
            head=parse_int(attr.get("head")),
            form=attr["form"],
            lemma=lemma,
            pos=pos,
            case=case,
            flags=tags,
            definition=lsj.get(lemma) if lemma else None,
        )

lsj = shelve.open("data/ag/lsj")

