import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from weedly_bot.loader import dp, api_client, bot
from weedly_bot.paths.my_subs.calldata import feeds_calldata


@dp.callback_query_handler(feeds_calldata.filter(action='turn_off'))
async def turn_off(call: types.CallbackQuery, callback_data: dict):
    user_id = call.from_user.id
    feed_id = callback_data['feed_id']
    feed_name = callback_data['feed_name']

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отключить еще уведомления',
                              callback_data='turn_off_noticiations')],

        [InlineKeyboardButton(text='< Назад',
                              callback_data='back_to_notifications')]]
    )
    req_result = api_client.users.turn_off_notifications_for_feed(
        user_id, feed_id)

    if req_result:

        await call.message.edit_text(text=f'Выключили уведомления для {feed_name}', reply_markup=kb)

    else:
        await call.message.edit_text(text=f'Не получилось выключить уведомления для {feed_name}. Давай попозже.', reply_markup=kb)
