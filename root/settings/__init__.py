"""
This is a django-split-settings main file.
For more information read this:

https://github.com/sobolevn/django-split-settings
Default environment is `developement`.
To change settings file:
`DJANGO_ENV=production python manage.py runserver`

"""

from os import environ

from split_settings.tools import include

ENV = environ.get('DJANGO_ENV') or 'development'

base_settings = [
    'components/middleware.py',  # middleware configuration
    'components/common.py',  # standard django settings
    'components/apps.py',  # installed applications
    'components/database.py',  # database settings
    'components/pyuploadcare.py',  # pyuploadcare settings
    'components/rest_framework.py',  # rest framework settings
    'components/allauth.py',  # allauth rest_auth settings
    'components/currency.py',  # currency settings
    'components/email.py',  # email settings
    'components/departments.py',
    'components/rest_framework.py',  # rest framework settings
]

# Include settings:

include(*base_settings)
