import re
import shelve
from itertools import dropwhile, pairwise, takewhile
from pathlib import Path
from typing import Generator, Type
from xml.etree.ElementTree import Element

from dominate.tags import p, span
from lxml import etree

from app.core.treebanks.ref import SubDoc

from ..utils import at
from .ref import Ref, RefRange, SubDoc, parse_subdoc
from .treebank import Paragraph, Sentence, Treebank
from .word import POS, Case, Word


class PerseusTreebank(Treebank):
    body: etree._Element
    gorman: bool
    _subdocs: list[Ref | RefRange] = []

    def __init__(
        self,
        f: Path,
        ref_cls: Type[Ref],
        gorman: bool = False,
        **kwargs,
    ) -> None:
        super().__init__(ref_cls=ref_cls, **kwargs)
        self.gorman = gorman

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

        self._subdocs = [
            parse_subdoc(self.ref_cls, subdoc)
            for sentence in self.body.findall(".//sentence")
            if (_subdoc := sentence.attrib.get("subdoc")) is not None
            and (subdoc := str(_subdoc)) != ""
        ]

    def __getitem__(self, ref: SubDoc | str) -> list[Sentence]:
        match ref:
            case str():
                return self[parse_subdoc(self.ref_cls, ref)]
            case RefRange(start, end):
                # TODO: make this more efficient / robust
                lstripped = dropwhile(lambda s: s.subdoc != start, self.sentences())
                rstripped = takewhile(lambda s: s.subdoc != end, lstripped)
                return list(rstripped)
            case Ref():
                if ref in self._subdocs:
                    el = self.body.find(
                        f".//sentence[@subdoc='{ref}']"
                    )  # TODO: paragraphs, etc.
                    if el is not None:
                        return [self.sentence(el)]  # type: ignore
                return []
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")
            
    def paragraphs(
        self, sentences: list[Sentence] | None
    ) -> Generator[Paragraph, None, None]:
        # TODO: make this actually work
        raise NotImplementedError

            
    def render_body(self, subdoc: SubDoc | None = None):
        for pg in (
            self.paragraphs(None)
            if subdoc is None
            else self.paragraphs(self[subdoc])
        ):
            with p():
                span(
                    ref := str(pg[0].subdoc),
                    data_subdoc=ref,
                    cls="subdoc",
                )
                for s in pg:
                    self.render_sentence(s)

    def render_sentence(self, sentence: Sentence):
        if self.meta.format == "verse":
            raise NotImplementedError()
        else:
            with span(cls="sentence"):
                for w, next in pairwise(sentence):
                    Word.render(w, next)
                Word.render(sentence[-1])

    def normalize_urn(self, urn: str | bytes) -> str:
        return re.search(r"^(urn:cts:greekLit:tlg\d{4}.tlg\d{3}).*", str(urn)).group(1)  # type: ignore

    def sentences(self) -> Generator[Sentence, None, None]:
        yield from (self.sentence(el) for el in self.body.findall(".//sentence"))  # type: ignore

    def sentence(self, el: Element) -> Sentence:
        words: list[Word] = [
            w for token in el if (w := _word(token.attrib)) is not None
        ]
        return Sentence(words, parse_subdoc(self.ref_cls, el.attrib["subdoc"]))


lsj = shelve.open("data/ag/lsj")  # TODO


def _word(attr: dict) -> Word | None:
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
        return int(s) if s != "" else None

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
