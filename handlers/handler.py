from aiogram import Router, types
from aiogram.filters import CommandStart
from database.orm_query import get_names_kb  # Функция для получения данных из БД
from kbds.reply import create_buttons_keyboard  # Импорт функции клавиатуры

# Создаем роутер для обработки команд
start_router = Router()
db_name = 'chapter'
@start_router.message(CommandStart())
async def send_buttons(message: types.Message):
    names = await get_names_kb(db_name=db_name)
    keyboard = create_buttons_keyboard(names)  # Создаем клавиатуру на основе данных
    await message.answer("Выберите опцию:", reply_markup=keyboard)
