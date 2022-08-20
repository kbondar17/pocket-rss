
import logging

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from weedly_bot.loader import dp, api_client
from weedly_bot.mystates import My_states
from weedly_bot import utils

logger = logging.getLogger(__name__)

@dp.message_handler(text_contains='Добавить источники')
@dp.callback_query_handler(text_contains='add_rss', state='*')
async def add_rss(call: types.CallbackQuery):
    """просим юзера отправить rss ссылку. входим в состояние typing и ловим ссылку"""

    await call.message.answer(text='пришли ссылку на rss-поток')
    await My_states.typing_rss.set()
    logger.debug('установили стейт typing_rss')

    await call.answer(cache_time=0)


@dp.message_handler(state=My_states.typing_rss)
async def typing_rss(message: types.Message, state: FSMContext):
    """ловим ссылку. валидируем. добавляем feed в БД, если его еще нет. 
       добавляем feed в подписки юзера. выходим из состояния ловли ссылки """

    await message.answer(f'Проверяем ссылку {message.text.strip()}')

    rss_link = message.text
    check_rss = utils.check_if_valid_rss_url(rss_link)
    user_id = message.from_user.id

    if check_rss['res']:

        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Добавить еще источник', callback_data='add_rss')],
                                                   [InlineKeyboardButton(text='< Назад', callback_data='choose_what_to_add')]])

        api_client.feeds.add_rss_source(rss_link)
        feed = api_client.feeds.get_by_url(rss_link)
        logger.debug('получили feed %s', feed)

        api_client.users.subscrbe_user_to_rss(uid=user_id, feed_id=feed['uid'])

    else:

        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отправить другую ссылку', callback_data='add_rss')],
                                                   [InlineKeyboardButton(
                                                       text='< Назад', callback_data='choose_what_to_add')]
                                                   ]
                                  )

    await state.reset_state()
    await message.answer(text=check_rss['msg'], reply_markup=kb)
