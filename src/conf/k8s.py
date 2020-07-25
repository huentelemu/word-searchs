from conf.base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB', 'huentelemu'),
        'USER': os.getenv('POSTGRES_USER', 'huentelemu'),
        'PASSWORD': os.getenv('POSTGRES_PASS', 'huentelemu'),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', 25060),
    }
}

STATIC_ROOT = '/huentelemu/static'
MEDIA_ROOT = '/huentelemu/media'