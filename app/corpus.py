from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from core import corpus
from core.render import HtmlDocumentRenderer

router = APIRouter()


@router.get("/{lang}")
async def get_index(lang: str):
    try:
        return corpus.index(lang)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown language {lang}")


@router.get("/{lang}/{slug}", response_class=HTMLResponse)
async def get_treebank(lang: str, slug: str, ref: str | None = None):
    try:
        tb = corpus.get_treebank(lang, slug)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown treebank {slug}")
    try:
        if ref is not None:
            tb = tb[ref]
        return HtmlDocumentRenderer(tb).render()
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unknown reference {ref}")
