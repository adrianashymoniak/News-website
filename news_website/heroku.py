from news_website.settings import *
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='DATABASE_URL'
    )
}

BROKER_URL = dj_database_url.config(
        default='REDIS_URL'
    )