from typing import TypeVar

T = TypeVar('T')
U = TypeVar('U')


def at(l: list[T] | None, i: int) -> T | None:
    if l is None:
        return None
    return l[i] if len(l) > i else None


def invert(d: dict[T, U]) -> dict[U, T]:
    return {v: k for k, v in d.items()}
