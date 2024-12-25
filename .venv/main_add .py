import aiogram
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
import asyncio
import Config
import texts
from Config import * #BOT_TOKEN, price_M, price_L, price_XL
from keyboards import *
from texts import *
import logging

logging.basicConfig(level=logging.INFO)

bot = Bot(token=Config.BOT_TOKEN)
dp  = Dispatcher(bot, storage= MemoryStorage())

@dp.message_handler(commands=["start"])
async def start(message):
    await message.answer(f"Добро пожаловать, {message.from_user.username} " + texts.start, reply_markup = start_kb)

#message.answer_photo
#message.answer_video
#message.answer_file

@dp.message_handler(text=["О нас"])
async def info(message):
    with open('img5.jpg', 'rb') as img:
        await message.answer_photo(img, texts.about, reply_markup = start_kb)

@dp.message_handler(text=["Стоимость"])
async def price(message):
    await message.answer("Что Вас интересует?", reply_markup = catalog_kb)

@dp.callback_query_handler(text="medium")
async def by_medium(call):
    await call.message.answer(texts.Mgame, reply_markup = by_kb)
    await call.answer()

@dp.callback_query_handler(text="big")
async def by_big(call):
    await call.message.answer(texts.Lgame, reply_markup = by_kb)
    await call.answer()

@dp.callback_query_handler(text="mega")
async def by_mega(call):
    await call.message.answer(texts.XLgame, reply_markup = by_kb)
    await call.answer()

@dp.callback_query_handler(text="other")
async def by_other(call):
    await call.message.answer(texts.other, reply_markup = by_kb)
    await call.answer()

@dp.callback_query_handler(text="back_to_catalog")
async def back(call):
    await call.message.answer("Что Вас интересует?", reply_markup = catalog_kb)
    await call.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
