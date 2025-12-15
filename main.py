import asyncio

from db_handler import create_database, remove_table
from handlers.client import client_register_handlers
from handlers.admin import admin_register_handlers
from config import dp, bot
from aiogram.methods import DeleteWebhook


async def main():
    print('Bot is online!✅')
    # remove_table()
    create_database()
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    client_register_handlers(dp)
    admin_register_handlers(dp)
    asyncio.run(main())
