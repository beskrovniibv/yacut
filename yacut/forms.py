from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from settings import MAX_URL_LENGTH, SHORT_URL_LENGTH


class URLMapForm(FlaskForm):
    original = StringField(
        'original',
        validators=[
            DataRequired(message='required'),
            Length(1, MAX_URL_LENGTH),
        ]
    )
    short = StringField(
        'short',
        validators=[
            Length(1, SHORT_URL_LENGTH),
            Optional(),
        ]
    )
    submit = SubmitField('get it!')
