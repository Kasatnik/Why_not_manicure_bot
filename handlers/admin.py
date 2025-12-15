from aiogram.types import FSInputFile

from config import bot
from aiogram import types, Dispatcher, F
from aiogram.filters.command import Command
from settings import ADMINS


async def cmd_start(message: types.Message):
    if message.from_user.id in ADMINS:
        file_db = FSInputFile('manicure_users.db')
        await bot.send_document(message.from_user.id, file=file_db, caption='Клиентская база данных.')


def admin_register_handlers(dp: Dispatcher):
    dp.message.register(cmd_start, Command('users'))
