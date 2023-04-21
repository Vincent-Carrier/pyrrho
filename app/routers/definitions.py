from fastapi import APIRouter

from app.lib.lexicon import LexiconEntry

router = APIRouter()

@router.get("/{lang}/{lemma}")
async def get_definition(lang: str, lemma: str):
    defs = await LexiconEntry.find(LexiconEntry.lemma == lemma).all()
    return {"definitions": defs}
