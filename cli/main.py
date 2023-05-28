import json
from dataclasses import asdict
from typing import Optional, TypeAlias

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from core import corpus
from core.constants import BUILD
from core.render import HtmlPartialRenderer, TerminalRenderer
from core.utils import filter_none

app = typer.Typer()
console = Console()

LangOpt: TypeAlias = Annotated[Optional[str], typer.Option()]


@app.command()
def ls(lang: LangOpt = None) -> None:
    """List all treebanks"""
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
def cat(lang: str, slug: str, ref: str) -> None:
    """Print a passage to stdin"""
    tb = corpus.get_treebank(lang, slug)
    passage = tb[ref]
    TerminalRenderer(passage).render()


app()
