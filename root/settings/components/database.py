
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.getcwd(), 'database.sqlite3'),
    }
}
