import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import DB_PATH, TELEGRAM_TOKEN
from database import DB
from handlers.chat import setup_chat_handlers
from handlers.common import setup_common_handlers


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher()
    db = DB(DB_PATH)
    await db.init()
    setup_common_handlers(dp, db)
    setup_chat_handlers(dp, bot, db)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
