import os

ALLOWED_HOSTS = ['kubierecki.pl', 'www.kubierecki.pl']
SECRET_KEY = os.environ['SECRET_KEY']
DEBUG = False

ADMINS = (
    ('Jan Kubierecki', 'jankubierecki@gmail.com'),
    ('Jan Kubierecki', 'admin@kubierecki.pl'),
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'partnerships',
        'USER': 'root',
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}

EMAIL_HOST = 'ssl0.ovh.net'
EMAIL_HOST_USER = 'admin@kubierecki.pl'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
SERVER_EMAIL = 'django@kubierecki.pl'
