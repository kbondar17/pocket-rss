import logging
from aiogram import types

from weedly_bot.paths.archive.search import calldata as author_calldata
from weedly_bot.paths.archive.search.keyborads.callback_data import choose_media_to_search_callback_data

from weedly_bot.loader import dp, api_client
from weedly_bot.utils import generators


logger = logging.getLogger(__name__)


@dp.callback_query_handler(author_calldata.filter())
async def author_pagination(call: types.CallbackQuery, callback_data:dict):
    """ callback_data = {'@': 'author', 'name': 'Маша Цепелева', 'uid': '43', 'page': '1'} """

    logger.debug('call.data --- %s', call.data)
    logger.debug('callback_data --- %s', callback_data)


    author_id = callback_data['uid']
    name = callback_data['name']
    page = callback_data['page']


    feed_name = api_client.authors.get_author_feed(author_id)['name']
    data_for_return = choose_media_to_search_callback_data.new(action='paginate_media', media=feed_name, page=1)

    articles = api_client.authors.get_articles_of_an_author(author_id)

    generator = generators.KeyboardGenerator()
    text, keyboard = generator.generate_articles(list_of_articles=articles,feed_name=feed_name,
                                                 author_name=name, data_for_pagination=callback_data,
                                                 current=int(page), data_for_return=data_for_return)

    await call.message.edit_text(text=text, reply_markup=keyboard, disable_web_page_preview=True)


