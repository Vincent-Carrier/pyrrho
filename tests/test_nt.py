from pyrrho.core.constants import AG
from pyrrho.core.corpus.ag import corpus
from pyrrho.core.nt.nt import GntTreebank

tb = GntTreebank(
    AG / "new-testament.conllu",
    title="New Testament",
)

def test_str():
    nt = corpus["nt"]()
    html = str(nt["MATT_1.1"])
    assert "Βίβλος" in html

