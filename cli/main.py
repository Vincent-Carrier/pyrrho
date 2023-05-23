import typer

from core.corpus.ag import corpus
from core.render.terminal import TerminalRenderer

app = typer.Typer()


@app.command()
def gnt() -> None:
    nt = corpus['nt']()
    passage = nt['JOHN_1']
    TerminalRenderer(passage).render()


app()
