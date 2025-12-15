from settings import TOKEN
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
