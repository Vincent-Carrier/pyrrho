import asyncio

from app.core.langs.ag.lexicon import seed_lsj


async def main():
    await seed_lsj()


asyncio.run(main())
