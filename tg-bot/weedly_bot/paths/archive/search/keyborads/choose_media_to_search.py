from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from weedly_bot.loader import api_client
from weedly_bot.paths.archive.search.keyborads.callback_data import choose_media_to_search_callback_data



def make_kb():
    """ИНЛАЙН КЛАВИАТУРА СО ВСЕМИ МЕДИА"""

    medias = api_client.feeds.get_all_smi_names()
    list_of_media_KB = InlineKeyboardMarkup(row_width=1)

    for m in medias:
        m = m.replace(':', '')
        list_of_media_KB.add(InlineKeyboardButton(text=m,
                                                  callback_data=choose_media_to_search_callback_data.new(
                                                      action='paginate_media',
                                                      media=m,
                                                      page=1)))

    list_of_media_KB.add(InlineKeyboardButton(text='< Назад', callback_data= 'back_to_choosing_source' ))

    return list_of_media_KB

