from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from app.core.langs.ag.corpus import corpus

router = APIRouter()


@router.get("/{lang}")
async def get_index(lang: str):
    match lang:
        case "ag":
            return {
                "treebanks": [
                    {"slug": slug, "title": entry.title, "author": entry.author}
                    for slug, entry in corpus.items()
                ]
            }
        case _:
            return HTTPException(status_code=404, detail=f"Unknown language {lang}")


@router.get("/{lang}/{slug}", response_class=HTMLResponse)
async def get_treebank(lang: str, slug: str, subdoc: str | None = None):
    if slug in corpus.keys():
        tb = corpus[slug]()
        if subdoc is None:
            return tb.render()
        else:
            return tb.render(subdoc=tb.parse_subdoc(subdoc))
    else:
        raise HTTPException(status_code=404, detail=f"Unknown treebank {slug}")
