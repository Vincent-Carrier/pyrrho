from abc import ABCMeta

class Token(Enum):
    SENTENCE_START = auto()
    SENTENCE_END = auto()
    PARAGRAPH_START = auto()
    PARAGRAPH_END = auto()
    LINE_BREAK = auto()


Renderable: TypeAlias = Word | RefPoint | Token
class Renderer(metaclass=ABCMeta):
    def body(self, Iterable[Renderable]) -> pre:
        ...

class HtmlRenderer():
    def body(self, Iterable[Renderable]) -> pre:
        ...
