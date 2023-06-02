from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.render import HtmlDocumentRenderer
from core import corpus

router = APIRouter()
api_router = APIRouter()


@router.get("/{lang}")
async def get_index(lang: str):
    try:
        return corpus.index(lang)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Unknown language {lang}") from e


@router.get("/{lang}/{slug}", response_class=HTMLResponse)
async def get_treebank(lang: str, slug: str, ref: str | None = None):
    try:
        tb = corpus.get_treebank(lang, slug)
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Unknown treebank {slug}") from e
    try:
        if ref is not None:
            tb = tb[ref]
        return HtmlDocumentRenderer(tb.meta).render()
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Unknown reference {ref}") from e
