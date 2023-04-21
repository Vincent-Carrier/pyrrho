from fastapi import APIRouter

from app.lib.langs.ag.lexicon import LsjEntry

router = APIRouter()

@router.get("/{lang}/{lemma}")
async def get_definition(lang: str, lemma: str):
    defs = await LsjEntry.get("01GYGRVW2T513VYERENJF77NEM")
    return {"definitions": defs}
