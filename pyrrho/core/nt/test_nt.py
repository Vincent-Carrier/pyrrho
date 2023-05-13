from ..constants import AG
from ..corpus.ag import corpus
from .nt import GntTreebank

tb = GntTreebank(
    AG / "new-testament.conllu",
    title="New Testament",
)

def test_str():
    nt = corpus["nt"]()
    html = str(nt["MATT_1.1"])
    assert "Βίβλος" in html
