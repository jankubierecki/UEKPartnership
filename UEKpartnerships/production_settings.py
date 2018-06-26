from .settings import *
import os

ALLOWED_HOSTS = [os.environ['DOMAIN'], 'www.' + os.environ['DOMAIN']]
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

ADMINS = (
    ('Jan Kubierecki', 'jankubierecki@gmail.com'),
)

MANAGERS = ADMINS

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
        'PASSWORD': 'postgres'
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
SERVER_EMAIL = os.environ['SERVER_MAIL']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
EMAIL_PORT = os.environ['EMAIL_PORT']
