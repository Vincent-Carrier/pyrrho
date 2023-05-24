from pytest import mark

from core.ref import BCV, CV, RefPoint, RefRange

eq_tests = [
    (BCV(1, 1, 1), BCV(1, 1, 1), True),
    (BCV(1, 1, 1), BCV(1, 2, 1), False),
    (CV(2, 1), CV(2, 1), True),
]


@mark.parametrize("a, b, expected", eq_tests)
def test_eq_ref(a: RefPoint, b: RefPoint, expected: bool):
    assert (a == b) == expected


lt_tests = [
    (BCV(1, 1, 1), BCV(1, 1, 1), False),
    (BCV(1, 1, 1), BCV(1, 2, 1), True),
    (BCV(1, 1, 1), BCV(2, 1, 1), True),
    (BCV(1, 1, 1), BCV(1, 1, 2), True),
]


@mark.parametrize("a, b, expected", lt_tests)
def test_lt_ref(a: RefPoint, b: RefPoint, expected: bool):
    assert (a < b) == expected


ref_contains_tests = [
    (BCV(1, 1, 1), BCV(1, 1, 1), True),
    (BCV(1, 1, None), BCV(1, 1, 1), True),
    (BCV(1, 1, None), BCV(1, 1, 2), True),
    (BCV(1, 1, 1), BCV(1, 2, None), False),
    (BCV(1, 1, 1), BCV(2, 1, None), False),
]


@mark.parametrize("a, b, expected", ref_contains_tests)
def test_ref_contains(a: RefPoint, b: RefPoint, expected: bool):
    assert (b in a) == expected


def test_parse():
    assert BCV.parse("1.1.1") == BCV(1, 1, 1)
    assert BCV.parse("1.1") == BCV(1, 1, None)
    assert CV.parse("1.1") == CV(1, 1)
    assert CV.parse("1") == CV(1)


def test_parse_range():
    assert RefRange.parse(BCV, "1.1.1-1.1.2") == RefRange(BCV(1, 1, 1), BCV(1, 1, 2))
