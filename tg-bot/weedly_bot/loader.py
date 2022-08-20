from dotenv import load_dotenv
import os
import logging
import logging.config
from yarl import URL

from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from weedly_bot.api.client import ApiClient


load_dotenv('../.env')
API_TOKEN = os.getenv('API_TOKEN')
API_URL = os.getenv('API_URL')
print('API_TOKEN  ----', API_TOKEN)
print('API_URL  ----', API_URL)

api_client = ApiClient(URL(API_URL))


bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)
