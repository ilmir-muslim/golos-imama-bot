from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile


from database.db_query import (
    add_file_id,
    fetch_chapter,
    fetch_theme,
    get_lesson_data,
)  # Функция для получения данных из БД
from database.engine import session_maker
from kbds.reply import get_keyboard  # Импорт функции клавиатуры


class MyRouter(Router):
    @staticmethod
    async def start_handler(message: types.Message):
        async with session_maker() as session:
            chapter_names = await fetch_chapter(session)
            keyboard = get_keyboard(
                *chapter_names,
                sizes=(3,),
            )  # Создаем клавиатуру на основе данных
            await message.answer("Выберите раздел:", reply_markup=keyboard)

    @staticmethod
    async def theme_handler(message: types.Message):
        async with session_maker() as session:
            chapter = message.text
            theme_names = await fetch_theme(session, chapter)
            keyboard = get_keyboard(
                *theme_names,
                sizes=(3,),
            )  # Создаем клавиатуру на основе данных
            await message.answer("Выберите тему:", reply_markup=keyboard)

    @staticmethod
    async def lesson_handler(message: types.Message):
        async with session_maker() as session:
            theme = message.text

            lessons = await get_lesson_data(session, theme)
            if lessons:
                for lesson in lessons:
                    await message.answer(lesson["name"])
                    await message.answer(lesson["annotation"])
                    if lesson["audiofile_id"] and lesson["text_file_id"]:
                        await message.answer_audio(audio=lesson["audiofile_id"])
                        await message.answer_document(document=lesson["text_file_id"])
                    else:
                        audio_path = f'/home/ilmir/dev_vscode/golos_imama/admin_panel/{lesson["audio_lesson"]}'
                        audio_file = FSInputFile(audio_path)
                        msg_a = await message.answer_audio(
                            audio_file, caption=lesson["name"]
                        )
                        audiofile_id = msg_a.audio.file_id

                        text_path = f'/home/ilmir/dev_vscode/golos_imama/admin_panel/{lesson["text_lesson"]}'
                        text_file = FSInputFile(text_path)
                        msg_t = await message.answer_document(
                            text_file, caption=lesson["name"]
                        )
                        text_file_id = msg_t.document.file_id

                        name = lesson["name"]
                        await add_file_id(session, name, audiofile_id, text_file_id)

            else:
                await message.answer("Нет данных по этой теме.")


start_router = MyRouter()

start_router.message.register(MyRouter.start_handler, CommandStart())
start_router.message.register(MyRouter.theme_handler, F.text == "тестовый раздел")
start_router.message.register(MyRouter.lesson_handler, F.text == "тестовая тема")
