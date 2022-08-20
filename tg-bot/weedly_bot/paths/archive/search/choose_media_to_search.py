from weedly_bot.loader import dp
from aiogram import types

from weedly_bot.paths.archive.search.keyborads.choose_media_to_search import make_kb

from weedly_bot.loader import logging
logger = logging.getLogger(__name__)


@dp.callback_query_handler(text_contains='search_by_media')
async def search_in_media(call: types.CallbackQuery):


    kb = make_kb()
    await call.message.answer(text='Выберите СМИ:', reply_markup=kb, parse_mode='Markdown')
