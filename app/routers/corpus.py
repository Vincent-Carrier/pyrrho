from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.core.langs.ag.corpus import corpus

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


@router.get("/{lang}/{slug}", response_class=HTMLResponse)
async def get_treebank(lang: str, slug: str, subdoc: str | None = None):
    if (tb := corpus.get(slug)) is not None:
        return tb().render(subdoc)
    else:
        raise HTTPException(status_code=404, detail=f"Unknown treebank {slug}")
