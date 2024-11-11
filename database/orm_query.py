from sqlalchemy import select
from sqlalchemy.ext.automap import automap_base

from database.engine import engine
from database.engine import session_maker


Base = automap_base()
Base.prepare(engine, reflect=True)

Chapter = Base.classes.chapter
Lesson = Base.classes.lesson   

async def get_chapter_kb():
    async with session_maker() as session:
        result = await session.execute(select(Chapter.name))
        names = result.scalars().all()
    return names

async def get_lesson_kb():
    async with session_maker() as session:
        result = await session.execute(select(Lesson.name))
        names = result.scalars().all()
    return names

