from aiogram.types import InputMediaPhoto

import texts.category
from keyboards import *


async def costs(message):
    with open('files/media/info.jpg', "rb") as img:
        await message.answer_photo(img, '<b>Выберите интересующую вас услугу</b>', parse_mode='HTML', reply_markup=catalog_kb)


async def manikur(call):
    with open('files/media/manikur.jpg', "rb") as img:
        mes = InputMediaPhoto(media=img, caption=texts.category.manikur, parse_mode='HTML')
        await call.message.edit_media(mes, reply_markup=buy_kb)
    await call.answer()


async def pedikur(call):
    with open('files/media/pedikur.jpg', "rb") as img:
        mes = InputMediaPhoto(media=img, caption=texts.category.pedikur, parse_mode='HTML')
        await call.message.edit_media(mes, reply_markup=buy_kb)
    await call.answer()


async def narast(call):
    with open('files/media/narast.png', "rb") as img:
        mes = InputMediaPhoto(media=img, caption=texts.category.narast, parse_mode='HTML')
        await call.message.edit_media(mes, reply_markup=buy_kb)
    await call.answer()


async def other(call):
    with open('files/media/other.png', "rb") as img:
        mes = InputMediaPhoto(media=img, caption=texts.category.other, parse_mode='HTML')
        await call.message.edit_media(mes, reply_markup=buy_kb)
    await call.answer()


async def back(call):
    with open('files/media/info.jpg', "rb") as img:
        mes = InputMediaPhoto(media=img, caption='<b>Выберите интересующую вас услугу</b>', parse_mode='HTML')
        await call.message.edit_media(mes, reply_markup=catalog_kb)
    await call.answer()