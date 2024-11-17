from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram import F

from database.db_query import fetch_chapter, fetch_theme  # Функция для получения данных из БД
from kbds.reply import get_keyboard  # Импорт функции клавиатуры

# Создаем роутер для обработки команд
start_router = Router()

@start_router.message(CommandStart())
async def send_chapter_btns(message: types.Message):
    names = await fetch_chapter()
    keyboard = get_keyboard(*names,sizes=(3, ),) # Создаем клавиатуру на основе данных
    await message.answer("Выберите раздел:", reply_markup=keyboard)
    

@start_router.message(F.text)
async def send_theme_btns(message: types.Message):
    chapter = message.text
    print(f'выбран раздел {chapter}')
    names = await fetch_theme(chapter=chapter)
    keyboard = get_keyboard(*names,sizes=(3, ),) # Создаем клавиатуру на основе данных
    await message.answer("Выберите тему:", reply_markup=keyboard)