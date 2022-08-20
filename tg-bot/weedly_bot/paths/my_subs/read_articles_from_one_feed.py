import logging
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from weedly_bot.paths.my_subs.calldata import feeds_calldata


from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators


logger = logging.getLogger(__name__)


comeback_kb = InlineKeyboardMarkup(
    inline_keyboard=[

        [InlineKeyboardButton(text='< Назад',
                              callback_data='show_user_feeds')],
    ]
)


@dp.callback_query_handler(feeds_calldata.filter(action='read'))
async def read_one_feed(call: types.CallbackQuery, callback_data: dict):
    logger.debug('call.data --- %s', call.data)
    logger.debug('callback_data --- %s', callback_data)

    feed_id = callback_data['feed_id']
    feed_name = callback_data['feed_name']
    page = callback_data['page']

    articles = api_client.feeds.get_all_articles_of_a_feed(feed_id)
    if not articles:
        await call.message.edit_text(text='Материалы грузятся. Заходи попозже',
                                     reply_markup=comeback_kb)

    else:

        generator = generators.KeyboardGenerator()
        text, kb = generator.generate_articles(list_of_articles=articles,
                                               data_for_return='show_user_feeds',
                                               feed_name=feed_name,
                                               data_for_pagination=callback_data,
                                               current=int(page))
        print('text-----', text)
        print('kb----', kb)
        await call.message.edit_text(text=text, reply_markup=kb, disable_web_page_preview=True)
