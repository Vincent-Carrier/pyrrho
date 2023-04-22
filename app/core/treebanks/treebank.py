from itertools import pairwise
from typing import Generator, TypeAlias

from boltons.iterutils import chunked_iter
from dominate.tags import *  # type: ignore
from lxml import etree
from word import *

from app.core.treebanks.ref import Ref


@dataclass
class Sentence:
    words: list[Word]
    subdoc: str = ""

    def __iter__(self):
        return iter(self.words)

    def __getitem__(self, index):
        return self.words[index]

    def __len__(self):
        return len(self.words)

Format = Literal["prose", "verse"]
Paragraph = list[Sentence]

@dataclass
class Metadata:
    slug: str
    title: str = "untitled"
    author: str = "unknown"
    urn: str | None = None
    start: Ref | None = None
    end: Ref | None = None

@dataclass
class Treebank:
    format: Format
    meta: Metadata

    def sentences(self) -> Generator[Sentence, None, None]:
        raise NotImplementedError("subclass must implement this method")

    def sentence(self, sentence: Sentence):
        raise NotImplementedError("subclass must implement this method")

    def normalize_subdoc(self, subdoc: str) -> str:
        # if self.meta.book:
        #     return f"{self.meta.book}.{subdoc}"
        # else:
        return subdoc

    def render(self) -> str:
        with pre(cls=f"greek {self.format} syntax", data_urn=self.meta.urn) as html:
            for pg in self.paragraphs:
                with p():
                    span(
                        subdoc := self.normalize_subdoc(pg[0].subdoc),
                        cls="subdoc",
                        data_subdoc=f"{subdoc}",
                    )
                    for s in pg:
                        self.sentence(s)

        return html.render()


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
                f"{w.form}{'' if next and next.pos == 'punctuation' else ' '}",
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
            words = []
            for word in s:
                w = parse_word(word.attrib)  # type: ignore
                if w:
                    words.append(w)
            yield Sentence(words, s.attrib.get("subdoc") or "")


class PROIEL_Treebank(Treebank):
    pass


class ConLL_Treebank(Treebank):
    pass
