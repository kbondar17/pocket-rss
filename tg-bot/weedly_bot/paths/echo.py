import logging
from aiogram import types

from weedly_bot.loader import dp


@dp.message_handler()
async def start(message: types.Message):
    print(message.text)
    await message.answer(f'{message.text} -- не понимаю. Воспользуйтесь командами из меню')
