import asyncio
from os import environ as env

from aredis_om import Migrator, get_redis_connection
from dotenv import load_dotenv

from app.lib.lexicon import LexiconEntry


async def init():
    load_dotenv()
    print("Running migrations...")
    await Migrator().run()
    LexiconEntry.Meta.database = get_redis_connection(
        url=env["REDIS_DATA_URL"], decode_responses=True, encoding="utf-8"
    )
