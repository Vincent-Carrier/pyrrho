from pytest import mark

from core.corpus import get_treebank
from core.ref import Ref
from core.treebank.nt import NT_BCV


@mark.slow
def test_str():
    nt = get_treebank("ag", "nt")
    html = str(nt["MATT_1.1"])
    assert "Βίβλος" in html


ref = lambda s: Ref(NT_BCV.parse(s))


@mark.parametrize(
    "a, b, expected",
    [
        (ref("MATT_1.1"), ref("MATT_1.2"), True),
        (ref("MATT_1.1"), ref("MATT_2"), True),
    ],
)
def test_compare_refs(a: Ref, b: Ref, expected: bool):
    assert (a < b) == expected
