from typing import Any, Protocol


class Renderer(Protocol):
    def render(self) -> Any:
        ...
