from .settings import *
import os

ALLOWED_HOSTS = [os.environ['DOMAIN'], 'www.' + os.environ['DOMAIN'], 'localhost', ]

SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

MIDDLEWARE_CLASSES = (
    'django_cas_ng.middleware.CASMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
)

CAS_SERVER_URL = "student.uek.krakow.pl"

ADMINS = (
    ('Jan Kubierecki', 'jankubierecki@gmail.com'),
)

MANAGERS = ADMINS

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'postgres',
        'PASSWORD': 'postgres'
    }
}

MAIL_NOTIFICATIONS = True

EMAIL_USE_TLS = False
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
SERVER_EMAIL = os.environ['SERVER_MAIL']
DEFAULT_FROM_EMAIL = os.environ['DEFAULT_FROM_EMAIL']
EMAIL_PORT = int(os.environ['EMAIL_PORT'])

sentry_sdk.init(
    dsn="https://77dfc23bd01b4ed3beb048b1c12b8c17@sentry.io/1406346",
    integrations=[DjangoIntegration()]
)
