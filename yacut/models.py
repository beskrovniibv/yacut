from datetime import datetime

import settings
from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(settings.MAX_URL_LENGTH), nullable=False)
    short = db.Column(db.String(settings.SHORT_URL_LENGTH), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=self.short,
        )
