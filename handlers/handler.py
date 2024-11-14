from aiogram import Router, types
from aiogram.filters import CommandStart
from database.db_query import fetch_data  # Функция для получения данных из БД
from kbds.reply import get_keyboard  # Импорт функции клавиатуры

# Создаем роутер для обработки команд
start_router = Router()

@start_router.message(CommandStart())
async def send_chapter(message: types.Message):
    names = await fetch_data('chapter')
    keyboard = get_keyboard(
    *names,
    # placeholder='выберете раздел',
    sizes=(2, ),
) # Создаем клавиатуру на основе данных
    await message.answer("Выберите раздел:", reply_markup=keyboard)
