from aiogram import Bot, Dispatcher
import asyncio
from config import TG_TOKEN
from app.handlers import root
import logging
import sys

bot = Bot(token=TG_TOKEN)
dp = Dispatcher()


dp.include_router(root)

async def main():
    logging.basicConfig(#level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler("bot.log"),
            logging.StreamHandler(sys.stdout)
])
    await dp.start_polling(bot)


asyncio.run(main())


    