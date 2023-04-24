import re
from itertools import dropwhile, pairwise, takewhile
from typing import Generator, Type
from xml.etree.ElementTree import Element

from dominate.tags import span
from lxml import etree

from .ref import Ref, RefRange, SubDoc
from .treebank import Metadata, Sentence, Treebank
from .word import Word, parse_word


class AgldTreebank(Treebank):
    body: etree._Element
    gorman: bool
    _subdocs: list[Ref | RefRange] = []

    def __init__(
        self,
        f: str,
        meta: Metadata,
        ref_cls: Type[Ref],
        gorman: bool = False,
    ) -> None:
        super().__init__(meta, ref_cls=ref_cls)
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
            self.parse_subdoc(subdoc)
            for sentence in self.body.findall(".//sentence")
            if (_subdoc := sentence.attrib.get("subdoc")) is not None
            and (subdoc := str(_subdoc)) != ""
        ]

    def __getitem__(self, ref: SubDoc | str) -> list[Sentence]:
        match ref:
            case str():
                return self[self.parse_subdoc(ref)]
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

    def render_sentence(self, sentence: Sentence):
        def word(w: Word, next: Word | None = None):
            span(
                f'{w.form}{"" if next and next.form in "".split(".,;:·") else " "}',
                cls=f"{w.pos if w.pos == 'verb' else ''} {w.case or ''}",
                data_id=str(w.id),
                data_head=str(w.head),
                data_lemma=w.lemma,
                data_def=w.definition,
                data_flags=w.flags,
            )

        if self.meta.format == "verse":
            raise NotImplementedError()
        else:
            with span(cls="sentence"):
                for w, next in pairwise(sentence):
                    word(w, next)
                word(sentence[-1])

    def normalize_urn(self, urn: str | bytes) -> str:
        return re.search(r"^(urn:cts:greekLit:tlg\d{4}.tlg\d{3}).*", str(urn)).group(1)  # type: ignore

    def sentences(self) -> Generator[Sentence, None, None]:
        yield from (self.sentence(el) for el in self.body.findall(".//sentence"))  # type: ignore

    def sentence(self, el: Element) -> Sentence:
        words: list[Word] = [
            w for token in el if (w := parse_word(token.attrib)) is not None
        ]
        return Sentence(words, self.parse_subdoc(el.attrib["subdoc"]))

    def parse_subdoc(self, subdoc: str) -> SubDoc:
        return (
            RefRange.parse(self.ref_cls, subdoc)
            if "-" in subdoc
            else self.ref_cls.parse(subdoc)
        )
