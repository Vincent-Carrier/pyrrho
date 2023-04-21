import asyncio
from os import environ as env

from aredis_om import Migrator, get_redis_connection
from dotenv import load_dotenv

from app.lib.langs.ag.lexicon import LsjEntry


async def init():
    load_dotenv()
    print("Running migrations...")
    await Migrator().run()
    LsjEntry.Meta.database = get_redis_connection(
        url=env["REDIS_DATA_URL"], decode_responses=True, encoding="utf-8"
    )
