import asyncio
import os

from aiogram import Bot, Dispatcher

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.handler import start_router

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

dp.include_router(start_router)


async def main():
    await dp.start_polling(bot)

asyncio.run(main())