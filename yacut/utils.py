from random import choice

from . import db
from .models import URLMap
from settings import ALLOWED_SYMBOLS


def get_unique_short_id(url):
    short = URLMap.query.get(original=url)
    if short is None:
        while short is None or URLMap.query.get(short=short).count != 0:
            for _ in range(6):
                short += choice(ALLOWED_SYMBOLS)
        return short, 201
    return short, 200
