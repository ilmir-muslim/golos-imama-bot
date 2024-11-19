from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


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
    SELECT lesson.name, lesson.annotation, lesson.audio_lesson, lesson.text_lesson, 
        telegram_file_id.audiofile_id, telegram_file_id.text_file_id
    FROM lesson  
    LEFT JOIN telegram_file_id ON telegram_file_id.name_id = lesson.id 
    WHERE lesson.theme_id = (SELECT id FROM theme WHERE name = :theme)
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
            "text_lesson": row[3],
            "audiofile_id": row[4],
            "text_file_id": row[5],
        }
        lessons.append(lesson)

    return lessons


async def add_file_id(session, name, audiofile_id, text_file_id):
    query = text(
        """ INSERT INTO telegram_file_id (name_id, audiofile_id, text_file_id) VALUES ((SELECT id FROM lesson WHERE name = :name) , :audiofile_id, :text_file_id) """
    )
    try:
        async with session.begin():
            await session.execute(
                query,
                {"name": name, "audiofile_id": audiofile_id, "text_file_id": text_file_id},
            )
            print(f"Inserting data: {name}, {audiofile_id}, {text_file_id}")

    except SQLAlchemyError as e:
        print(f"Ошибка при выполнении SQL-запроса: {e}")
