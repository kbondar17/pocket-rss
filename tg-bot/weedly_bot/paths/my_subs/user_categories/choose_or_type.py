from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators


@dp.callback_query_handler(text_contains='read_category')
async def choose(call: types.CallbackQuery):



    choose_source_kb = InlineKeyboardMarkup(
        inline_keyboard=[

            [InlineKeyboardButton(text='Выбрать один источник', callback_data='show_user_feeds')],
            [InlineKeyboardButton(text='Выбрать катеогорию', callback_data='read_category')],
            [InlineKeyboardButton(text='Читать все в одной ленте', callback_data='read_all')],
            [InlineKeyboardButton(text='< Назад', callback_data='back_to_start')],

        ]

    )



