import asyncio

from aredis_om import get_redis_connection

from app.core.langs.ag.lexicon import seed_lsj

from .app.main import init


async def main():
    await init()
    redis = await get_redis_connection()
    redis.flushall()
    await seed_lsj()

asyncio.run(main())
