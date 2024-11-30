from sqlalchemy import text


async def fetch_chapter(session):
    query = text("SELECT name FROM chapter")
    async with session.begin():
        result = await session.execute(query)
    names = [row[0] for row in result]
    return names


async def fetch_theme(session, chapter):
    query = text(
        """
        SELECT name 
        FROM theme 
        WHERE chapter_id = (SELECT id FROM chapter WHERE name = :chapter)
    """
    )
    async with session.begin():
        result = await session.execute(query, {"chapter": chapter})
    names = [row[0] for row in result]
    return names


async def get_lesson_data(session, theme):
    # Выполняем запрос для получения данных из базы данных
    query = text(
        """
    SELECT name, annotation, audio_lesson, audiofile_id
    FROM lesson
    WHERE theme_id = (SELECT id FROM theme WHERE name = :theme)
    """
    )
    async with session.begin():
        result = await session.execute(query, {"theme": theme})
    lessons = []
    for row in result:
        lesson = {
            "name": row[0],
            "annotation": row[1],
            "audio_lesson": row[2],
            "audiofile_id": row[3],
        }
        lessons.append(lesson)

    return lessons
