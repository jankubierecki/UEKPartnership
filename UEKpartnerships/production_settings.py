from .settings import *
import os
ALLOWED_HOSTS = ['kubierecki.pl', 'www.kubierecki.pl', '46.101.53.236', 'web']
SECRET_KEY = os.environ['SECRET_KEY']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'partnerships',
        'USER': 'root',
        'PASSWORD': os.environ['DB_PASSWORD'],
    }
}
