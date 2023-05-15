from pytest import mark

from core import nt
from core.constants import AG
from core.corpus.ag import corpus
from core.ref import Ref

tb = nt.TB(
    AG / "new-testament.conllu",
    title="New Testament",
)

@mark.slow
def test_str():
    nt = corpus["nt"]()
    html = str(nt["MATT_1.1"])
    assert "Βίβλος" in html


ref = lambda s: Ref(nt.BCV.parse(s))


@mark.parametrize(
    "a, b, expected",
    [
        (ref("MATT_1.1"), ref("MATT_1.2"), True),
        (ref("MATT_1.1"), ref("MATT_2"), True),
    ],
)
def test_compare_refs(a: Ref, b: Ref, expected: bool):
    assert (a < b) == expected
