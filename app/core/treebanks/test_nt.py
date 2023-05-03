from pathlib import Path

from .nt import NT_Treebank

tb = NT_Treebank(
    Path("data/ag") / "new-testament.conllu",
    title="New Testament",
)

def test_getitem():
    assert str(tb['MATT_1.1'][0]) == 'Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ'
    assert ". ".join(str(s) for s in tb['MATT_1'][:2]) == 'Βίβλος γενέσεως Ἰησοῦ Χριστοῦ υἱοῦ Δαυεὶδ υἱοῦ Ἀβραάμ. Ἀβραὰμ ἐγέννησεν τὸν Ἰσαάκ'
    assert str(tb['JOHN_1.1'][0]) == 'Ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὸν θεόν καὶ θεὸς ἦν ὁ λόγος'
    assert ". ".join(str(s) for s in tb['JOHN_1'][:2]) == 'Ἐν ἀρχῇ ἦν ὁ λόγος καὶ ὁ λόγος ἦν πρὸς τὸν θεόν καὶ θεὸς ἦν ὁ λόγος. οὗτος ἦν ἐν ἀρχῇ πρὸς τὸν θεόν'
