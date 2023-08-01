from random import choice

from settings import ALLOWED_SYMBOLS

from . import db
from .models import URLMap


def get_unique_short_id(url):
    short = URLMap.query.filter_by(original=url).first()
    if short is None:
        while short is None or URLMap.query.filter_by(short=short).count() != 0:
            short = ''
            for _ in range(6):
                short += choice(ALLOWED_SYMBOLS)
        return short, 201
    return short.short, 200
