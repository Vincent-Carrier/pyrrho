from app import init
from app.lib.langs.ag.lexicon import seed_lsj


async def main():
    await init()
    await seed_lsj()
