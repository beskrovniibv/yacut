from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from settings import MAX_URL_LENGTH, SHORT_URL_LENGTH, SHORT_URL_PATTERN


class URLMapForm(FlaskForm):
    original_link = StringField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, MAX_URL_LENGTH),
        ]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, SHORT_URL_LENGTH, message='Короткая ссылка может содержать от 1 до 16 символов'),
            Optional(strip_whitespace=False),
            Regexp(regex=SHORT_URL_PATTERN, message='Ссылка содержит недопустимые символы')
        ]
    )
    submit = SubmitField('Создать')
