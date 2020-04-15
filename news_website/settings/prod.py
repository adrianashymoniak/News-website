from .base import *

DATABASES = {
    'default': dj_database_url.config(
        default='DATABASE_URL'
    )
}

BROKER_URL = dj_database_url.config(default='REDIS_URL')
CELERY_RESULT_BACKEND = dj_database_url.config(default='REDIS_URL')