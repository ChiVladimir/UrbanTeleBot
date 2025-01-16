import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from config import *
from keyboards import *
from admin import *
from db import *
import texts

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

#-----------------ADMIN-----------------------

admins = [410011143]


@dp.message_handler(commands=['admin'])
async def admin(message):
    if message.from_user.id in admins:
        await message.answer("Панель Адмнистратора", reply_markup=admin_panel)
    else:
        await message.answer("Вы не являетесь Админом!", reply_markup=None)


@dp.message_handler(text="users")
async def users(call):
    await call.message.answer(show_users(cursor,connection))
    await call.answer()


@dp.message_handler(text="stat")
async def stat(call):
    await call.message.answer(show_stat(cursor,connection))
    await call.answer()


class UserState(StatesGroup):
    id = State()


@dp.callback_query_handler(text="block")
async def block_user(call):
    await call.message.answer("Введите id пользователя")
    await UserState.id.set()
    await call.answer()


@dp.message_handler(state=UserState.id)
async def block_st(message,state):
    input_id = message.text
    add_to_block(input_id, cursor,connection)
    await message.answer("Пользователь с указанным id был заблокирован")
    await state.finish()


class UserStateU(StatesGroup):
    id = State()


@dp.callback_query_handler(text="block")
async def unblock_user(call):
    await call.message.answer("Введите id пользователя")
    await UserStateU.id.set()
    await call.answer()


@dp.message_handler(state=UserStateU.id)
async def unblock_st(message, state):
    input_id = message.text
    remove_block(input_id, cursor,connection)
    await message.answer("Пользователь с указанным id был раззаблокирован")
    await state.finish()


#-----------------END-ADMIN--------------------

#----------------Main------------------------
@dp.message_handler(commands=["start"])
async def start(message):
    add_user(message.from_user.id,message.from_user.username,message.from_user.username, cursor,connection)
    await message.answer(f"Добро пожаловать, {message.from_user.username}! " + texts.start, reply_markup=start_kb)



#message.answer_photo
#.answer_video
#.answer_file

@dp.message_handler(text="О нас")
async def price(message):
    with open('files/4.png', "rb") as img:
        await message.answer_photo(img, texts.about, reply_markup=start_kb)


@dp.message_handler(text="Стоимость")
async def info(message):
    await message.answer("Что вас интересует ?", reply_markup=catalog_kb)


@dp.callback_query_handler(text="medium")
async def buy_m(call):
    await call.message.answer(texts.Mgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="big")
async def buy_l(call):
    await call.message.answer(texts.Lgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="mega")
async def buy_xl(call):
    await call.message.answer(texts.XLgame, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="other")
async def buy_other(call):
    await call.message.answer(texts.other, reply_markup=buy_kb)
    await call.answer()


@dp.callback_query_handler(text="back_to_catalog")
async def back(call):
    await call.message.answer("Что вас интересует ?", reply_markup=catalog_kb)
    await call.answer()


#------------------END-MAIN----------------------


if __name__ == "__main__":
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    executor.start_polling(dp, skip_updates=True)
    connection.commit()
    connection.close()
