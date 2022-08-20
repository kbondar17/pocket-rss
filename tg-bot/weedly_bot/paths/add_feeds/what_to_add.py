import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from weedly_bot.loader import dp

logger = logging.getLogger(__name__)


add_rss_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Подписаться на RSS поток',
                          callback_data='add_rss')],
    [InlineKeyboardButton(text='< Назад', callback_data='back_to_start')]
], row_width=1
)

@dp.message_handler(text_contains='Добавить источники')
async def what_to_add(message: types.Message):

    await message.answer('Что добавляем?', reply_markup=add_rss_kb)


@dp.callback_query_handler(text_contains='choose_what_to_add')
async def what_to_add_callback(call: types.CallbackQuery):

    await call.message.answer('Что добавляем?', reply_markup=add_rss_kb)
