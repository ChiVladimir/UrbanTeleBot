import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
import Config

bot = Bot(token=Config.BOT_TOKEN)
dp  = Dispatcher(bot, storage= MemoryStorage())

class UserState(StatesGroup):
    address = State()

kb = ReplyKeyboardMarkup()
button_inf = KeyboardButton( text='Информация')
button_start = KeyboardButton( text='Начало')

kb.add(button_inf)
kb.add(button_start)
#kb.row kb.insert

kb_in = InlineKeyboardMarkup()
button_in = InlineKeyboardButton(text='Информация', callback_data='Info')

kb_in.add(button_in)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Info', callback_data='Info')],
        [KeyboardButton(text ='Shop'),
         KeyboardButton(text ='Donate')
            ]
    ], resize_keyboard=True
)

HELP = """
/help - вывести справку по программе.
/start - начать процесс бронирования.
/id - запрос персонального идентификационного номера.
/add - добавить новое бронирование.
/show - показать все бронирования.
/exit - выход.
"""

@dp.message_handler(commands=["help"])
async def help(message):
    await message.answer(f'{HELP}')

@dp.message_handler(commands=["start"])
async def send_welcome(message):
    print(f"Пользователь {message.from_user.id} начал процесс бронирования")
#    await message.answer('Привет! Я - специальный заказывающий бот.', reply_markup = kb_in)
    await message.answer('Привет! Я - специальный заказывающий бот.', reply_markup = start_menu)

@dp.callback_query_handler(text = 'Info')
async def infor(call):
    await call.message.answer(f'{HELP}')
    await call.answer()

#@dp.message_handler(text='Информация')
#async def inform(message):
#    await message.answer (HELP)

@dp.message_handler(text='Начало')
async def inform(message):
    print('Новое бронирование! Делаем запрос адреса')
    await message.reply('Отлично! Перед началом бронирования мне нужен адрес доставки. Введи адрес, пожалуйста!')
    await UserState.address.set()


@dp.message_handler(commands=["id"])
async def start_handler(message: types.Message):
    print(f"Пользователь {message.from_user.id} запросил номер ID")
    await message.answer(f"Твой ID: {message.from_user.id}")

@dp.message_handler(commands=["add"])
async def send_welcome(message: types.Message):
    print('Новое бронирование! Делаем запрос адреса')
    await message.reply('Отлично! Перед началом бронирования мне нужен адрес доставки. Введи адрес, пожалуйста!')
    await UserState.address.set()

@dp.message_handler(state=UserState.address)
async def fsm_handler(message, state):
    await state.update_data(first = message.text)
    data = await state.get_data()
    print(f'Адрес доставки - {data["first"]}')
    await message.answer(f'Адрес доставки будет: {data["first"]}')
    await state.finish()

@dp.message_handler()
async def all_message(message: types.Message):
    print("Новый пользователь")
    await message.reply("Выберете /start или /help для начала")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
