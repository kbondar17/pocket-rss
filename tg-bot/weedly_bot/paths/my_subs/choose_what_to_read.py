from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from weedly_bot.loader import dp

choose_source_kb = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(
            text='Выбрать один источник', callback_data='show_user_feeds')],

        [InlineKeyboardButton(
            text='Читать все в одной ленте', callback_data='read_all')],
        [InlineKeyboardButton(
            text='Отписаться от источника', callback_data='unsb')],
        [InlineKeyboardButton(
            text='< Назад', callback_data='back_to_start')],

    ]

)


@dp.message_handler(text_contains='Читать подписки')
async def choose_source(message: types.Message):

    await message.answer('Как читать?', reply_markup=choose_source_kb)


@dp.callback_query_handler(text_contains='back_to_choosing_source')
async def choose_source_callback(call: types.CallbackQuery):

    await call.message.edit_text('Как читать?', reply_markup=choose_source_kb)
