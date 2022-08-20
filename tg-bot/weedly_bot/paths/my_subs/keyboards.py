from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def generate_who_to_read_kb(authors):



    who_to_read_kb = InlineKeyboardMarkup(
        inline_keyboard= [

            [InlineKeyboardButton(text='Выбрать издание', callback_data='choose_a_media')],
            [InlineKeyboardButton(text='Выбрать автора', callback_data = 'choose_an_author')],

        ]
    )


what_to_read_kb = InlineKeyboardMarkup(
    inline_keyboard= [

        [InlineKeyboardButton(text='Выбрать издание', callback_data='choose_a_media')],
        [InlineKeyboardButton(text='Выбрать автора', callback_data = 'choose_an_author')],

    ]
)



