from pathlib import Path

from ..langs.ag.corpus import corpus
from .nt import NT_Treebank

tb = NT_Treebank(
    Path("data/ag") / "new-testament.conllu",
    title="New Testament",
)

def test_str():
    nt = corpus["nt"]()
    html = str(nt["MATT_1.1"])
    assert "Βίβλος" in html

