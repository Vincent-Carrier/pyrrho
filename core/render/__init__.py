from typing import Any, Protocol

from .html import StandaloneRenderer
from .terminal import TerminalRenderer


class Renderer(Protocol):
    def render(self) -> Any:
        ...
