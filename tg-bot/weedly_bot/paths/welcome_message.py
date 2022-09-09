import logging
# from loguru import logger
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from weedly_bot.loader import dp
from weedly_bot.loader import api_client

import logging
logger = logging.getLogger(__name__)

main_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='📝 Добавить источники'),
                                           KeyboardButton(text='📖 Читать подписки')],
                                          [KeyboardButton(text='❓ О боте'),
                                           KeyboardButton(text='🔔 Настроить уведомления')],
                                          ], row_width=2
                                )

welcome_text = '*Это Pocket RSS*\n\n'\
               'Хватит залипать в рекомендательных потоках. Читай только то, что действительно важно.\n\n'\
               '*Как это работает:* \n\nПришли ссылки RSS-фидов любимых изданий и сайтов и читай их в Телеграме. \n\n'\
               'В подписках уже добавлены несколько тестовых источников.\n\n'\
               'Скоро появится функция уведомлений о новых публикациях. Stay tuned!'


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """первое сообщение"""
    user_id = message.from_user.id
    user_name = message.from_user.username
    logger.debug('юзер %s нажал на старт', message.from_user.id)

    if not api_client.users.check_if_user_exists(uid=user_id):
        api_client.users.add_user(uid=user_id, name=user_name)
        api_client.users.add_test_rss(uid=user_id)

    await message.answer(text=welcome_text, reply_markup=main_menu, parse_mode='Markdown')


@dp.callback_query_handler(text_contains='back_to_start')
async def start_2(call: types.CallbackQuery):
    await call.message.answer(text=welcome_text, reply_markup=main_menu, parse_mode='Markdown')


@dp.message_handler(text_contains='О боте')
async def start(message: types.Message):
    await message.answer(text=welcome_text, reply_markup=main_menu, parse_mode='Markdown')
