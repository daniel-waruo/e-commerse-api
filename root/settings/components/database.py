
# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
import os

from root.settings.components.common import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),
    }
}
