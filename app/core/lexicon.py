from aredis_om import Field, JsonModel
from attr import dataclass


class LexiconEntry(JsonModel):
    lemma: str = Field(index=True)
    definitions: list[str]

@dataclass
class Lexicon:
    lang: str

    async def get_entry(self, lemma: str):
        return await LexiconEntry.find(LexiconEntry.lemma == lemma).first()
