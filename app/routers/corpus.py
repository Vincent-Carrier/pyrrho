from dataclasses import asdict

from fastapi import APIRouter, HTTPException

from app.core.langs.ag.corpus import corpus

router = APIRouter()


@router.get("/{lang}/{slug}")
async def get_treebank(lang: str, slug: str, subdoc: str | None = None):
    if slug in corpus.keys():
        tb = corpus[slug]
        return { **asdict(tb.meta), "body": tb.render() }
    else:
        raise HTTPException(status_code=404, detail=f"Unknown treebank {slug}")
