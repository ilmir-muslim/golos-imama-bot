from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



def create_buttons_keyboard(names):
    buttons = [[KeyboardButton(text=name)] for name in names]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

