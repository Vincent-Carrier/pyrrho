from typing import Any, TypeVar

T = TypeVar('T')
U = TypeVar('U')


def at(l: list[T] | None, i: int) -> T | None:
    if l is None:
        return None
    return l[i] if len(l) > i else None

def cx(*args: Any) -> str | None:
    return " ".join(str(a) for a in args if a) or None

def invert(d: dict[T, U]) -> dict[U, T]:
    return {v: k for k, v in d.items()}
