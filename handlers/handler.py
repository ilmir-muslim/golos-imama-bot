import os
from aiogram import Router, types, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from database.db_query import fetch_chapter, fetch_theme, get_lesson_data
from database.engine import session_maker
from kbds.reply import get_keyboard, navigation_keyboard

bot = Bot(token=os.getenv("TOKEN"))


storage = MemoryStorage()
router = Router()


# Состояния пользователя
class UserStates(StatesGroup):
    selecting_chapter = State()
    selecting_theme = State()
    viewing_lessons = State()






# Хендлер для /start
@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    async with session_maker() as session:
        chapter_names = await fetch_chapter(session)
        keyboard = navigation_keyboard(*chapter_names, sizes=(3,))
        await message.answer("Выберите раздел:", reply_markup=keyboard)
        await state.set_state(UserStates.selecting_chapter)


# Хендлер для выбора раздела
@router.message(UserStates.selecting_chapter)
async def chapter_handler(message: types.Message, state: FSMContext):
    if message.text == "В начало":
        await state.clear()  # Сброс состояния
        await start_handler(message, state)
        return

    async with session_maker() as session:
        chapter = message.text
        theme_names = await fetch_theme(session, chapter)
        keyboard = navigation_keyboard(*theme_names, sizes=(3,))
        await message.answer("Выберите тему:", reply_markup=keyboard)
        await state.update_data(selected_chapter=chapter)
        await state.set_state(UserStates.selecting_theme)


# Хендлер для выбора темы
@router.message(UserStates.selecting_theme)
async def theme_handler(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        async with session_maker() as session:
            chapter_names = await fetch_chapter(session)
            keyboard = navigation_keyboard(*chapter_names, sizes=(3,))
            await message.answer("Выберите раздел:", reply_markup=keyboard)
            await state.set_state(UserStates.selecting_chapter)
        return

    if message.text == "В начало":
        await state.clear()  # Сброс состояния
        await start_handler(message, state)
        return

    async with session_maker() as session:
        theme = message.text
        lessons = await get_lesson_data(session, theme)

        if lessons:
            for lesson in lessons:
                await message.answer(lesson["name"])
                await message.answer(lesson["annotation"])
                await message.answer_audio(audio=lesson["audiofile_id"])
        else:
            await message.answer("Нет данных по этой теме.")
        
        keyboard = get_keyboard("Назад", "В начало", sizes=(2,))
        await message.answer("Выберите действие:", reply_markup=keyboard)


# Регистрация маршрутов
router.message.register(start_handler)
router.message.register(chapter_handler, UserStates.selecting_chapter)
router.message.register(theme_handler, UserStates.selecting_theme)
