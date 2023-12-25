import urllib.parse
from datetime import datetime

from yacut import db

LOCAL_URL = 'http://localhost'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=urllib.parse.urljoin(LOCAL_URL, self.short),
        )

    def from_dict(self, data):
        self.original = data['url']
        self.short = data['short_link']
