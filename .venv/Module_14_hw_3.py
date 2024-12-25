#Домашнее задание по теме "Доработка бота"

import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import Config

bot = Bot(token=Config.BOT_TOKEN)
dp  = Dispatcher(bot, storage= MemoryStorage())
formula = '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
HELP = """
Бот для нахождения нормы суточного потребления калорий для человека.
Необходимо вести ваши параметры и бот рассчитает рекомендацию для вас.
Нажимайте на кнопку [Рассчитать] и начинайте процесс.
"""

class UserState(StatesGroup):
    age = State()
    growth= State()
    weight = State()

# Клавиатуры

#

button_start = KeyboardButton(text='Рассчитать')
button_inf = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_inf, button_start).add(button_buy)

#

button_count = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formula = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb_in = InlineKeyboardMarkup(resize_keyboard=True).row(button_count, button_formula)

#

button_prod_1 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button_prod_2 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button_prod_3 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button_prod_4 = InlineKeyboardButton(text='Product4', callback_data='product_buying')

kb_products = InlineKeyboardMarkup(resize_keyboard=True).row(button_prod_1, button_prod_2, button_prod_3, button_prod_4)


# Диалог


@dp.message_handler(commands=["start"])
async def main_menu(message):
    await message.answer('Я - специальный бот для нахождения нормы суточного потребления калорий для человека.', reply_markup=greet_kb)

@dp.message_handler(text="Рассчитать")
async def set_start(message):
    await message.answer('Выберите опцию', reply_markup = kb_in)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer(f'{formula}')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст, пожалуйста! ')
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
    if not data["age"].isdigit() or not data["weight"].isdigit() or not data["growth"].isdigit():
        await message.answer(f'Введенные данные некорректны! Должны быть только числа. '
                             f'Выберете /start для повтора или нажмите [Рассчитать]')
        await state.finish()
    else:
        result = int(10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
        await message.answer(f"Ваша норма в сутки {result} ккал")
        await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'Files/Prod_{i}.png', 'rb') as img:
            await message.answer_photo(img, f'\nНазвание: Product{i} | Описание: описание {i} | Цена: {i * 100}')
    await message.answer('Выберите продукт для покупки:', reply_markup = kb_products)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

@dp.message_handler(text='Информация')
async def set_info(message):
    await message.answer(HELP)

@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer("Добрый день! Выберете /start для начала")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

