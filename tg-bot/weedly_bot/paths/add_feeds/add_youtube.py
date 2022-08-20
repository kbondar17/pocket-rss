import logging
import feedparser
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from weedly_bot.loader import dp, api_client
from weedly_bot.mystates import My_states
from weedly_bot import utils

logger = logging.getLogger(__name__)


@dp.callback_query_handler(text_contains='add_youtube', state='*')
async def add_yt_channel(call: types.CallbackQuery):

    await call.message.answer(
        text='Пришли ссылку на канал, на который хочешь подписаться')
    await My_states.send_youtube.set()
    logger.debug('установили стейт send_youtube')

    await call.answer(cache_time=0)


@dp.message_handler(state=My_states.send_youtube)
async def typing_youtube(message: types.Message, state: FSMContext):

    await message.answer('Проверяем ссылку!')
    await state.reset_state()
    try:
        user_link = message.text
        u_id = message.from_user.id

        yt_rss_link = api_client.youtube.get_rss_link_from_yt_link(user_link)
        yt_name = feedparser.parse(yt_rss_link)['entries'][0]['author']

        api_client.feeds.add_rss_source(
            url=yt_rss_link, name=yt_name)

        feed_id = api_client.feeds.get_by_url(rss_url=yt_rss_link)['uid']
        user_subscription = api_client.users.subscrbe_user_to_rss(
            u_id, feed_id)

        if user_subscription:

            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отправить еще ссылку', callback_data='add_youtube')],
                                                       [InlineKeyboardButton(
                                                        text='< Назад', callback_data='choose_what_to_add')]
                                                       ]
                                      )

            await message.answer(text='Подписались!', reply_markup=kb)

        else:
            kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отправить другую ссылку', callback_data='add_youtube')],
                                                       [InlineKeyboardButton(
                                                        text='< Назад', callback_data='choose_what_to_add')]
                                                       ]
                                      )

            await message.answer(text='Неправильная ссылка!', reply_markup=kb)

    except Exception as ex:
        logging.debug(ex)
        await message.answer('Не получилось :(\nпопробуй попозже')
