from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb = InlineKeyboardMarkup(
    inline_keyboard= [

        [InlineKeyboardButton(text='📇 Добавить rss-источник', callback_data='nul:add_rss')],
        [InlineKeyboardButton(text='📺 Добавить Youtube-канал', callback_data='nul:search_by_youtube')],
        [InlineKeyboardButton(text='🔎 Искать авторов по изданию', callback_data = 'nul:search_by_media')],

    ]

)

#[InlineKeyboardButton(text='🔝 Посмотреть популярных авторов', callback_data='search_popular')],
# print(media_or_author_KB.to_python())

# '🔎','❓','📬'
