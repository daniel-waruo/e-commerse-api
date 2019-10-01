"""
This is a django-split-settings main file.
For more information read this:

https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`

"""

from split_settings.tools import optional, include
from os import environ

ENV = environ.get('DJANGO_ENV') or 'development'

base_settings = [
    'components/apps.py',  # installed applications
    'components/common.py',  # standard django settings
    'components/database.py',  # database settings
    'components/pyuploadcare.py',  # pyuploadcare settings
    'components/rest_framework.py',  # rest framework settings
    'components/allauth.py',  # allauth rest_auth settings
    'components/currency.py',  # currency settings
    'components/email.py',  # email settings
    'components/rest_framework.py'  # rest framework settings
]

# Include settings:
include(*base_settings)
