import logging
import os
from dotenv import load_dotenv
from pathlib import Path


# load_dotenv(Path(__file__).parents[1] / 'local.env')
load_dotenv(Path(__file__).parents[1] / 'prod.env')
print('DB_URL --- ',os.environ.get('DB_URL'))
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')

SQLALCHEMY_TRACK_MODIFICATIONS = False

# server settings
DEBUG = bool(os.getenv('DEBUG', 'False'))
APP_PORT = int(os.getenv('APP_PORT', '5000'))
APP_HOST = os.getenv('APP_HOST', '0.0.0.0')

my_log_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'

logging.basicConfig(level=logging.DEBUG, format=my_log_format)
