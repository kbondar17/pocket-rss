from aiogram import types

from weedly_bot.loader import dp
from weedly_bot.loader import logging, api_client
from weedly_bot.utils.generators import KeyboardGenerator
from weedly_bot.paths.archive.search.keyborads.callback_data import choose_media_to_search_callback_data

logger = logging.getLogger(__name__)
kb_generator = KeyboardGenerator()


@dp.callback_query_handler(choose_media_to_search_callback_data.filter())
async def media_pagination(call: types.CallbackQuery, callback_data:dict=None):
    """получили из клавы choose_media_to_search колбэк дату формата {'action', 'media', 'page'} """

    logger.debug('вошли в pagination с колдатой: %s', call.data)
    logger.debug('вошли в pagination с callback_data: %s', callback_data)

    media = callback_data['media']
    current_page = int(callback_data['page'])

    logger.debug('--- media ---: %s', media)
    logger.debug('--- current_page ---: %s', current_page)

    authors = api_client.feeds.get_all_authors_of_a_feed(media)

    kb = kb_generator.generate_authors(list_of_authors=authors, data_for_pagination=callback_data, current=current_page,
                                       data_for_entitites='author', data_for_return='search_by_media',
                                       num_of_entities_per_page=6)


    await call.message.edit_text(text = f'Вот авторы издания {media}', reply_markup= kb)

