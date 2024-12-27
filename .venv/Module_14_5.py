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
from crud_functions import get_all_products, is_included, add_user

bot = Bot(token=Config.BOT_TOKEN)
dp  = Dispatcher(bot, storage= MemoryStorage())
formula = '10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5'
HELP = """
Бот для нахождения нормы суточного потребления калорий для человека.
Необходимо вести ваши параметры и бот рассчитает рекомендацию для вас.
Нажимайте на кнопку [Рассчитать] и начинайте процесс.
Для приобретения БАД необходимо пройти регистрацию.
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
button_reg = KeyboardButton(text='Регистрация')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_inf, button_start, button_reg).add(button_buy)

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
    get_prod = get_all_products()
    for i in range(len(get_prod)):
        with open(f'Files/Prod_{i + 1}.png', 'rb') as img:
            await message.answer_photo(img, f'Название: {get_prod[i][1]} | Описание: {get_prod[i][2]} |  Цена: {get_prod[i][3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup = kb_products)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()
    check_user = is_included(data['username'])
    if check_user is False:#True:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer('Регистрация прошла успешно!', reply_markup=greet_kb)
    await state.finish()

@dp.message_handler(text='Информация')
async def set_info(message):
    await message.answer(HELP)

@dp.message_handler()
async def all_message(message: types.Message):
    await message.answer("Добрый день! Выберете /start для начала")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)