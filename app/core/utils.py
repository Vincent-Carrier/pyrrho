from typing import TypeVar

T = TypeVar('T')
def at(l: list[T] | None, i: int) -> T | None:
    if l is None:
        return None
    return l[i] if len(l) > i else None
