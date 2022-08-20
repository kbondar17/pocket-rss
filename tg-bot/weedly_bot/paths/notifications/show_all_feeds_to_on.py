import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators
from weedly_bot.paths.my_subs.calldata import feeds_calldata


@dp.callback_query_handler(text_contains='turn_on_noticiations')
async def show_user_feeds(call: types.CallbackQuery):
    '''показать все фиды юзера'''
    all_sources = api_client.users.get_user_feeds(uid=call.from_user.id)
    logging.debug('all_sources--- %s', all_sources)

    if not all_sources:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='< Назад',
                                  callback_data='back_to_notifications')]])

        await call.message.edit_text(text='В твоих подписках пусто. '
                                          'Подпишись на фиды в разделе меню "Добавить источники"',
                                          reply_markup=kb)

    current = 1
    if '#' in call.data:
        current = int(call.data.split('#')[1])

    kb_generator = generators.KeyboardGenerator()

    kb = kb_generator.generate_feeds(feeds=all_sources, current=current, feeds_calldata=feeds_calldata,
                                     data_for_return='back_to_notifications',
                                     data_for_pagination='turn_on_noticiations', action_for_calldata='turn_on')
    await call.message.edit_text(text='Выбери источник:', reply_markup=kb)
