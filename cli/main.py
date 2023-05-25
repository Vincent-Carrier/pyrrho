import json
from dataclasses import asdict
from typing import Optional, TypeAlias

import typer
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated

from core import corpus
from core.constants import BUILD
from core.render import HtmlRenderer, TerminalRenderer
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


@app.command()
def build(lang: str, slug: str) -> None:
    tb = corpus.get_treebank(lang, slug)
    dir = BUILD / lang / slug
    m = dir / "metadata.json"
    obj = filter_none(asdict(tb.meta))
    m.write_text(json.dumps(obj, indent=2))
    for chunk in tb.chunks():
        dir.mkdir(parents=True, exist_ok=True)
        f = dir / f"{chunk.meta.ref}.html"
        f.write_text(HtmlRenderer(chunk).render())


app()
