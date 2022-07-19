import os
from secrets import token_hex

from app import create_app
from config import get_settings

settings = get_settings()
app = create_app(config={
    'DEBUG': True,
    'SERVER_NAME': '127.0.0.1:8000',
    'SQLALCHEMY_DATABASE_URI': str(settings.CELERY_DBURI),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'JSON_AS_ASCII': False,

    'SECRET_KEY': os.getenv('SECRET_KEY', token_hex(16))
})
