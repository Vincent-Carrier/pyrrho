from typing import Any, Protocol

from .html import HtmlDocumentRenderer, HtmlPartialRenderer
from .terminal import TerminalRenderer


class Renderer(Protocol):
    def render(self) -> Any:
        ...
