import re

from flask import jsonify, request, url_for
from flask_api import status

from settings import SHORT_URL_LENGTH, SHORT_URL_PATTERN

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/<string:short>/', methods=['GET', ])
def get_original_url(short):
    url = URLMap.query.filter_by(short=short).first()
    if url is not None:
        return jsonify({'url': url.original}), status.HTTP_200_OK
    raise InvalidAPIUsage('Указанный id не найден', status.HTTP_404_NOT_FOUND)


@app.route('/api/id/', methods=['POST', ])
def create_short():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    url = data.get('url')
    custom = data.get('custom_id')
    short, _ = (custom.strip(), status.HTTP_201_CREATED) if custom is not None and custom.strip() != '' else get_unique_short_id(url)
    if (
        len(short) > SHORT_URL_LENGTH or
        not re.match(SHORT_URL_PATTERN, short)
    ):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    # 
    if URLMap.query.filter_by(short=custom).first() is not None:
        raise InvalidAPIUsage(f'Имя "{custom}" уже занято.')
    if URLMap.query.filter_by(original=url).first() is not None and custom:
        raise InvalidAPIUsage(f'Для адреса {url} уже есть короткая ссылка')
    urlmap = URLMap(
        original=url,
        short=short,
    )
    db.session.add(urlmap)
    db.session.commit()
    urlmap.short = url_for('redirect_view', short=short, _external=True)
    return jsonify(urlmap.to_dict()), status.HTTP_201_CREATED