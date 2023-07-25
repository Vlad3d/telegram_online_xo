import asyncio
import logging
import db_connection

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import types

import config
from handlers import router


async def main():
    db_connection.init_db()
    bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    await set_main_menu(bot)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def set_main_menu(bot: Bot):
    main_menu_commands = [types.BotCommand(
                                command="/startgame",
                                description="Начать игру"
                          ),
                          types.BotCommand(
                                command="/endgame",
                                description="Закончить игру"
                          )]
    await bot.set_my_commands(main_menu_commands)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())