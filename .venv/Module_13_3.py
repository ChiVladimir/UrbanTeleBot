#Домашнее задание по теме "Машина состояний".

import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio
import Config

bot = Bot(token=Config.BOT_TOKEN)
dp  = Dispatcher(bot, storage= MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth= State()
    weight = State()

HELP = """
Бот для нахождения нормы суточного потребления калорий для человека.
Необходимо вести ваши параметры и бот рассчитает рекомендацию для вас.
/calories - начать процесс.
"""

@dp.message_handler(commands=["help"])
async def help(message):
    await message.answer(f'{HELP}')

@dp.message_handler(commands=["calories"])
async def set_age(message):
    print(f"Пользователь {message.from_user.id} начал ввод данных")
    await message.reply('Я - специальный бот для нахождения нормы суточного потребления калорий для человека.\n'
                        'Введите свой возраст, пожалуйста! ')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост, пожалуйста! ' )
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес, пожалуйста! ')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    print(f'Возраст - {data["age"]}, Рост - {data["growth"]}, Вес - {data["weight"]}')
    result = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f"Ваша норма в сутки {result} ккал")
    await state.finish()

@dp.message_handler()
async def all_message(message: types.Message):
    print("Новый пользователь")
    await message.reply("Добрый день! Выберете /calories или /help для начала")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
