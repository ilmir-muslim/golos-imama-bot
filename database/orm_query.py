from sqlalchemy import select, text
from sqlalchemy.ext.automap import automap_base

from database.engine import engine
from database.engine import session_maker


Base = automap_base()
Base.prepare(engine, reflect=True)

Chapter = Base.classes.chapter
Theme = Base.classes.theme   



async def get_chapter_kb():
    async with session_maker() as session:
        result = await session.execute(select(Chapter.name))
        names = result.scalars().all()
    return names


async def get_theme_kb(chapter:str):
    async with session_maker() as session:
        themes_query = text(f"SELECT name FROM theme WHERE chapter_id = (SELECT id FROM chapter WHERE name = {chapter})")
        result = await session.execute(themes_query, {"chapter": chapter})
        names = result.scalars().all()
    return names

