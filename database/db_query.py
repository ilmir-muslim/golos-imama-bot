import asyncpg
import asyncio

async def fetch_data(db_name):
    names = []
    conn = await asyncpg.connect (
        database="golos_imama",
        user="ilmir",
        password="230103",
        host="localhost",
        port=5432
    )
    async with conn.transaction():
        rows = await conn.fetch(f"SELECT name FROM {db_name}")
        names = [row['name'] for row in rows]
        

    await conn.close()
    return names