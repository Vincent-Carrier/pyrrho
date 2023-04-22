import pytest

from .ref import BCV, CV, Ref

eq_tests = [
    (BCV(1, 1, 1), BCV(1, 1, 1), True),
    (BCV(1, 1, 1), BCV(1, 2, 1), False),
    (CV(2,1), CV(2,1), True),
]

@pytest.mark.parametrize("a, b, expected", eq_tests)
def test_eq_ref(a: Ref, b: Ref, expected: bool):
    assert (a == b) == expected

lt_tests = [
    (BCV(1, 1, 1), BCV(1, 1, 1), False),
    (BCV(1, 1, 1), BCV(1, 2, 1), True),
    (BCV(1, 1, 1), BCV(2, 1, 1), True),
    (BCV(1, 1, 1), BCV(1, 1, 2), True), 
]

@pytest.mark.parametrize("a, b, expected", lt_tests)
def test_lt_ref(a: Ref, b: Ref, expected: bool):
    assert (a < b) == expected

ref_contains_tests = [
    (BCV(1, 1, 1), BCV(1, 1, 1), True),
    (BCV(1, 1, None), BCV(1, 1, 1), True),
    (BCV(1, 1, None), BCV(1, 1, 2), True),
    (BCV(1, 1, 1), BCV(1, 2, None), False),
    (BCV(1, 1, 1), BCV(2, 1, None), False),
]

@pytest.mark.parametrize("a, b, expected", ref_contains_tests)
def test_ref_contains(a: Ref, b: Ref, expected: bool):
    assert (b in a) == expected
