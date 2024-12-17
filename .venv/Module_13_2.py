import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from importlib.resources import files
from pprint import pprint
import Config

# name = 'bot_token.txt'
# file = open(name, 'r')
# api = file.read()
# file.close()
#
# bot = Bot(token=api)
bot = Bot(token=Config.BOT_TOKEN)
dp  = Dispatcher(bot, storage= MemoryStorage())

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    print('Привет! Я бот помогающий твоему здоровью.')
    await message.reply("Привет! Я бот помогающий твоему здоровью.")

@dp.message_handler()
async def all_message(message: types.Message):
    print("Введите команду /start, чтобы начать общение.")
    await message.reply("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
