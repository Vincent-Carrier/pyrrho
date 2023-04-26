import shelve

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{lang}/{lemma}")
async def get_definition(lang: str, lemma: str):
    with shelve.open("data/ag/lsj.db") as db:
        if lemma not in db:
            raise HTTPException(status_code=404, detail=f"Lemma {lemma} not found")
        return {"definitions": db[lemma].definitions}
