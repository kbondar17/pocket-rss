import logging
import os
# db settings
# SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL', 'postgresql://app:1441@localhost:5432/weedly',)
# SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL', 'postgresql://app:1441@localhost:5432/weedly',)
# SQLALCHEMY_DATABASE_URI = 'postgresql://app:1441@localhost:5432/weedly'
# SQLALCHEMY_DATABASE_URI ='postgresql://weedly:1441@http://127.0.0.1:5432/weedly'
# SQLALCHEMY_DATABASE_URI = 'postgresql://app:1441@localhost:5432/weedly'
SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL', 'postgresql://app:1441@db:5432/weedly')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# server settings
DEBUG = bool(os.getenv('DEBUG', 'False'))
APP_PORT = int(os.getenv('APP_PORT', '5000'))
APP_HOST = os.getenv('APP_HOST', '0.0.0.0')

my_log_format = '%(asctime)s %(name)s %(levelname)s: %(message)s'

logging.basicConfig(level=logging.DEBUG, format=my_log_format)
