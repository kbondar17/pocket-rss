from calendar import c
import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators


@dp.callback_query_handler(text_contains='show_notifications')
async def show_all_notifications(call: types.CallbackQuery):

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='< Назад',
                              callback_data='back_to_notifications')]])

    user_id = call.from_user.id
    feeds = api_client.users.get_user_notifications(user_id)

    if not feeds:
        await call.message.edit_text('Уведомления не настроены', reply_markup=kb)
    else:
        text = '*Уведомления приходят для:* \n'
        for i, feed in enumerate(feeds):
            text += f'{i+1}. {feed["name"]}\n'
        await call.message.edit_text(text=text, reply_markup=kb, parse_mode='Markdown')
