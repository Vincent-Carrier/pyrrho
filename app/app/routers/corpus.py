from functools import cache

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

import pyrrho.corpus as corpus
from pyrrho import StandaloneRenderer, Treebank

router = APIRouter()


# @router.get("/{lang}")
# async def get_index(lang: str):
#     match lang:
#         case "ag":
#             return {
#                 "treebanks": [
#                     {"slug": slug, "title": entry.meta.title, "author": entry.meta.author}
#                     for slug, entry in corpus.items()
#                 ]
#             }
#         case _:
#             return HTTPException(status_code=404, detail=f"Unknown language {lang}")

renderer = StandaloneRenderer()

@router.get("/{lang}/{slug}", response_class=HTMLResponse)
async def get_treebank(lang: str, slug: str, ref: str | None = None):
    if (tb := _get_treebank(slug)) is not None:
        if ref is not None:
            tb = tb[ref]
        return renderer.render(tb)
    else:
        raise HTTPException(status_code=404, detail=f"Unknown treebank {slug}")


@cache
def _get_treebank(slug) -> Treebank | None:
    return tb() if (tb := corpus.ag.get(slug)) is not None else None
