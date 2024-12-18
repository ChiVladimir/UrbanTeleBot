import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = "8110042185:AAERDVOgOu7wPQieCCHMX-oCgONG7T438Oc"
bot = Bot(token=api)
dp  = Dispatcher(bot, storage= MemoryStorage())

@dp.message_handler(text = ['Urban', 'ff'])
async def urban_message(message):
    print('Urban message')
    await message.answer('Urban message')

@dp.message_handler(commands = ['start'])
async def start_message(message):
    print('Start message')
    await message.answer('Hello! Nice to see you!')

@dp.message_handler()
async def all_message(message):
    print("Have a new message")
    await message.answer(message.text.upper())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
