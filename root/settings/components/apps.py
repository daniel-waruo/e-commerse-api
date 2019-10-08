INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # THIRD PARTY APPS
    # django money
    'djmoney',
    'djmoney.contrib.exchange',
    # session framework
    'qsessions',
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
    # business apps
    'business.inventory',
    'business.cms',
    'business.delivery',
    'business.orders',
    'business.payment',
    # client apps
    'client.checkout',
    'client.cart',
    # utils
    'utils.geo.phone_numbers',
    'utils.session'
]
