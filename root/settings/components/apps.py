INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # THIRD PARTY APPS
    # rest framework
    'rest_framework',
    'rest_framework.authtoken',

    # all auth
    'allauth',
    'allauth.account',

    # rest auth
    'rest_auth',
    'rest_auth.registration',

    # Custom Apps
    # auth
    'accounts',
    # business
    # 'business.delivery',
    # 'business.cms',
    # 'business.orders',
    # 'business.transactions'
    # utils
    'utils.geo.phone_numbers'
]
