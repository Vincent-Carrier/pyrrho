import typer
from rich.table import Table

from core import corpus
from core.render.terminal import TerminalRenderer, console

app = typer.Typer()


@app.command()
def ls() -> None:
    table = Table()
    table.add_column("slug")
    table.add_column("title")
    table.add_column("author")
    for slug, meta in corpus.index().items():
        table.add_row(slug, meta.title, meta.author)
    console.print(table)


@app.command()
def preview(slug: str, ref: str) -> None:
    tb = corpus.get_treebank(slug)
    passage = tb[ref]
    TerminalRenderer(passage).render()


app()
