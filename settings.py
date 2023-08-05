import os
import re

MAX_URL_LENGTH = 2000
SHORT_URL_LENGTH = 16

ALLOWED_SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

SHORT_URL_PATTERN = re.compile(r'^[{allowed}]{{1,{max_len}}}$'.format(allowed=ALLOWED_SYMBOLS, max_len=SHORT_URL_LENGTH))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', default='DEFAULT_SECRET')
