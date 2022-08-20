import logging
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators


import logging
logger = logging.getLogger(__name__)


comeback_kb = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text='< Назад',
                              callback_data='show_user_feeds')],
    ]
)


@dp.callback_query_handler(text_contains='read_all')
async def read_all_feeds(call: types.CallbackQuery):

    current = 1
    if '#' in call.data:
        current = call.data.split('#')[-1]
    logger.debug('call.data --- %s', call.data)

    user_id = call.from_user.id
    feeds = api_client.users.get_user_feeds(user_id)

    feeds_ids = [e['uid'] for e in feeds]

    all_feeds_articles = []
    for f_id in feeds_ids:
        articles = api_client.feeds.get_all_articles_of_a_feed(f_id)
        all_feeds_articles.append(articles)

    if not all_feeds_articles:
        await call.message.edit_text(text='Материалы грузятся. Заходи попозже',
                                     reply_markup=comeback_kb)
    else:

        all_feeds_articles = sum(all_feeds_articles, [])

        generator = generators.KeyboardGenerator()
        text, kb = generator.generate_articles(list_of_articles=all_feeds_articles,
                                               data_for_return='show_user_feeds',
                                               feed_name='',
                                               data_for_pagination='read_all',
                                               current=int(current))

        text = text[10:]
        await call.message.edit_text(text=text, reply_markup=kb, disable_web_page_preview=True)

    '''    {'author_id': 1, 'description': None, 'feed_id': 1, 'published': 'Sun, 16 Jan 2022 19:45:00 GMT',
        'title': 'Поправки на QRспективу // Какие изменения уже предложены в законопроект о «сертификатах здоровья»', 'uid': 12,
        'url': 'https://www.kommersant.ru/doc/5171005'}
    '''

#    await call.message.answer('читаем один')
