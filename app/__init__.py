from os import environ as env

from aredis_om import Migrator, get_redis_connection
from dotenv import load_dotenv

from app.lib.lexicon import LexiconEntry


async def init():
    load_dotenv()
    print("Running migrations...")
    redis = get_redis_connection()
    await Migrator().run()
