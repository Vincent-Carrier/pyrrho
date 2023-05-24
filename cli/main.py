from typing import Optional, TypeAlias

import typer
from rich.table import Table
from typing_extensions import Annotated

from core import corpus
from core.render.terminal import TerminalRenderer, console

app = typer.Typer()

LangOpt: TypeAlias = Annotated[Optional[str], typer.Option()]

@app.command()
def ls(lang: LangOpt = None) -> None:
    """List all treebanks."""
    table = Table()
    table.add_column("slug")
    table.add_column("title")
    table.add_column("author")
    if lang is None:
        table.add_column("lang")
    for slug, meta in corpus.index(lang).items():
        table.add_row(slug, meta.title, meta.author, *filter(None, [meta.lang]))
    console.print(table)


@app.command()
def preview(lang: str, slug: str, ref: str) -> None:
    tb = corpus.get_treebank(lang, slug)
    passage = tb[ref]
    TerminalRenderer(passage).render()


app()
