
import logging
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from weedly_bot.loader import dp
from weedly_bot.loader import api_client

import logging
logger = logging.getLogger(__name__)


kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text='Посмотреть уведомления', callback_data='show_notifications')],
        [InlineKeyboardButton(
            text='Включить уведомления', callback_data='turn_on_noticiations')],
        [InlineKeyboardButton(
            text='Отключить уведомления', callback_data='turn_off_noticiations')],
        [InlineKeyboardButton(
            text='< Назад', callback_data='back_to_start')],

    ]

)

text = 'Что надо сделать?'


@dp.message_handler(text_contains='Настроить уведомления')
async def notifications(message: types.Message):
    await message.reply('Эта функция скоро появится!')
#     await message.edit_text(text=text, reply_markup=kb)


# @dp.callback_query_handler(text_contains='back_to_notifications')
# async def back_to_notifications(call: types.CallbackQuery):

#     await call.message.edit_text(text=text, reply_markup=kb)
