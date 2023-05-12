import re
from copy import copy
from pathlib import Path
from typing import Iterator, Self, Type, cast, final

from lxml import etree

from .constants import LSJ
from .ref import Ref, RefPoint, RefRange, T
from .token import FormatToken
from .treebank import Token, Treebank
from .utils import at, parse_int
from .word import POS, Case, Word


@final
class TB(Treebank[T]):
    body: etree._Element
    gorman: bool
    refs: list[Ref] = []

    def __init__(
        self,
        f: Path,
        ref_cls: Type[RefPoint],
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
                self.meta.urn = self.body.find("./sentence").attrib.get("document_id")  # type: ignore
            if self.meta.urn:
                self.meta.urn = self.normalize_urn(self.meta.urn)

            self.refs = [
                self.parse_ref(ref)
                for sentence in self.body.findall("./sentence")
                if (r := sentence.attrib.get("subdoc")) is not None
                and (ref := str(r)) != ""
            ]

    def __getitem__(self, ref: Ref | str) -> Self:
        if isinstance(ref, str):
            return self[self.parse_ref(ref)]
        match ref.value:
            case RefRange() | RefPoint() as r:
                if ref not in self:
                    raise KeyError(f"Cannot find {ref} in {self}")
                tb = copy(self)
                tb.ref = ref
                return tb
            case _:
                raise TypeError(f"Cannot get {ref} from {self}")

    def __contains__(self, ref: Ref) -> bool:
        return True  # TODO

    def sentences(self) -> Iterator[etree._Element]:
        if self.ref:
            match self.ref.value:
                case RefRange() as rr:
                    yield self.body.find(f"./sentence[@subdoc='{rr.start}']")  # type: ignore
                    path = f"./sentence[@subdoc='{rr.start}']/following-sibling::sentence"
                    for s in cast(Iterator[etree._Element], self.body.xpath(path)):  
                        if self.parse_ref(s.get("subdoc")) > rr.end:  # type: ignore
                            break
                        yield s
                case RefPoint() as rp:
                    yield self.body.find(f"./sentence[@subdoc='{rp}']")  # type: ignore
        else:
            yield from self.body.findall("./sentence")

    def __iter__(self) -> Iterator[Token]:
        # TODO: yield paragraph tokens
        for s in self.sentences():
            yield FormatToken.SENTENCE_START
            yield from (w for el in s.findall("./word") if (w := self.word(el.attrib)))
            yield FormatToken.SENTENCE_END

    def normalize_urn(self, urn: str | bytes) -> str:
        return re.search(r"^(urn:cts:greekLit:tlg\d{4}.tlg\d{3}).*", str(urn)).group(1)  # type: ignore

    def word(self, attr) -> Word | None:
        if attr.get("insertion_id") is not None:  # TODO
            return None

        tags = attr.get("postag")
        pos = POS.parse_agldt(at(tags, 0))
        case = Case.parse_agldt(at(tags, 7))

        lemma = attr.get("lemma")
        if lemma:
            lemma = re.sub(r"\d+$", "", lemma)

        ref = None
        cite = attr.get("cite")
        if cite:
            

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


lsj = LSJ()
