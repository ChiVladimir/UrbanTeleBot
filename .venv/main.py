import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "8110042185:AAERDVOgOu7wPQieCCHMX-oCgONG7T438Oc"
bot = Bot(token=api)
dp  = Dispatcher(bot, storage= MemoryStorage())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
