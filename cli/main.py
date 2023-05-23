import typer

from core.corpus.ag import corpus
from core.render.terminal import TerminalRenderer

app = typer.Typer()


@app.command()
def preview(treebank: str, ref: str) -> None:
    tb = corpus[treebank]()
    passage = tb[ref]
    TerminalRenderer(passage).render()


app()
