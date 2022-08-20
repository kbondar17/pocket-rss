import logging
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators

from weedly_bot.paths.my_subs.calldata import feeds_calldata


import logging


@dp.callback_query_handler(feeds_calldata.filter(action='unsb'))
async def unsubscribe(call: types.CallbackQuery, callback_data: dict):
    logging.debug(f'вошли в unsubscribe с колдатой {call.data}')
    feed_id = callback_data['feed_id']
    user_id = call.from_user.id

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text='Удалить еще источник', callback_data='unsb')],
        [InlineKeyboardButton(text='< Назад',
                              callback_data='back_to_choosing_source')]])

    unsubscribe_res = api_client.users.unsubcribe_user_from_rss(
        user_id, feed_id)

    if unsubscribe_res:

        await call.message.edit_text(text='Отписались!', reply_markup=kb)

    else:
        await call.message.answer(text='Не получилось отписаться. Попробуй попозже', reply_markup=kb)


@ dp.callback_query_handler(text_contains='unsb')
async def list_all_sources(call: types.CallbackQuery):
    logging.debug('вошли в list_all_sources')

    all_sources = api_client.users.get_user_feeds(uid=call.from_user.id)

    if not all_sources:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='< Назад',
                                  callback_data='back_to_choosing_source')]])

        await call.message.edit_text(text='В твоих подписках пусто. '
                                     'Подпишись на фиды в разделе меню "Добавить источники"', reply_markup=kb)

    current = 1
    if '#' in call.data:
        current = int(call.data.split('#')[1])

    kb_generator = generators.KeyboardGenerator()
    kb = kb_generator.generate_feeds(feeds=all_sources, current=current, feeds_calldata=feeds_calldata,
                                     data_for_return='back_to_choosing_source',
                                     data_for_pagination='unsb', action_for_calldata='unsb')
    await call.message.edit_text(text='Выбери от кого отписаться:', reply_markup=kb)
