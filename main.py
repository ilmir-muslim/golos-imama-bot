import asyncio
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv

from database.engine import session_maker
from middlewares.db import DataBaseSession
from handlers.handler import start_router
load_dotenv(find_dotenv())


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(start_router)


async def main():
    await dp.start_polling(bot, skip_updates=True)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

asyncio.run(main())