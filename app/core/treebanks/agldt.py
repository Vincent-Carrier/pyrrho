from itertools import pairwise
from typing import Generator

from dominate.tags import *  # type: ignore
from lxml import etree

from app.core.treebanks.treebank import Format, Metadata, Sentence, Treebank
from app.core.treebanks.word import Word, parse_word, re


class AgldTreebank(Treebank):
    root: etree._Element
    gorman: bool

    def __init__(
        self,
        f: str,
        meta: Metadata,
        format: Format = "prose",
        gorman: bool = False,
    ) -> None:
        super().__init__(format, meta)
        self.gorman = gorman

        tree = etree.parse(f)
        self.root = tree.getroot()
        self.meta.urn = self.root.attrib.get("cts")
        if self.meta.urn is None:
            self.meta.urn = self.root.find(".//sentence").attrib.get("document_id")  # type: ignore
        if self.meta.urn:
            self.meta.urn = self.normalize_urn(self.meta.urn)

    def sentence(self, sentence: Sentence):
        def tag(w: Word, next: Word | None = None):
            span(
                w.form + "" if next and next.form in "".split(".,;:") else " ",
                cls=f"{w.pos if w.pos == 'verb' else ''} {w.case or ''}",
                data_id=str(w.id),
                data_head=str(w.head),
                data_lemma=w.lemma,
                data_def=w.definition,
                data_flags=w.flags,
            )

        if self.format == "verse":
            raise NotImplementedError()
            # with p(style='display: inline;'):
            #     new_line = False
            #     verse_num = sentence[0].loc and sentence[0].loc.verse
            #     for w, next in pairwise(sentence):
            #         if w.loc:
            #             verse_num = w.loc.verse
            #         if next.loc and next.loc.verse != verse_num:
            #             new_line = True
            #         tag(w, next)
            #         if next.loc and new_line:
            #             br()
            #             new_line = False
            #     tag(sentence[-1])
        else:
            with span(cls="sentence"):
                for w, next in pairwise(sentence):
                    tag(w, next)
                tag(sentence[-1])

    def normalize_urn(self, urn: str) -> str:
        return re.search(r"^(urn:cts:greekLit:tlg\d{4}.tlg\d{3}).*", urn).group(1)  # type: ignore

    def sentences(self) -> Generator[Sentence, None, None]:
        for s in self.root.findall(".//sentence"):
            words: list[Word] = [w := parse_word(token.attrib) for token in s if w is not None]  # type: ignore
            yield Sentence(words, s.attrib.get("subdoc") or "")
