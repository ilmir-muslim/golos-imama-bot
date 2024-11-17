import asyncpg
import asyncio


async def fetch_chapter():
    names = []
    conn = await asyncpg.connect(
        database="golos_imama",
        user="ilmir",
        password="230103",
        host="localhost",
        port=5432,
    )

    async with conn.transaction():
        rows = await conn.fetch("SELECT name FROM chapter")
        names = [row["name"] for row in rows]

    await conn.close()
    return names

async def fetch_theme(chapter):
    names = []
    conn = await asyncpg.connect(
        database="golos_imama",
        user="ilmir",
        password="230103",
        host="localhost",
        port=5432,
    )

    async with conn.transaction():
        rows = await conn.fetch(f"SELECT name FROM theme WHERE chapter_id = (SELECT id FROM chapter WHERE name = '{chapter}')")
        names = [row["name"] for row in rows]

    await conn.close()
    return names
