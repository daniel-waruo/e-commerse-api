INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
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
    # Knox integration
    'knox',
    # C.O.R.S management framework,
    'corsheaders',
    # all auth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.instagram',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # graphene
    'graphene_django',

    # rest auth
    'rest_auth',
    'rest_auth.registration',

    # Custom Apps
    # auth
    'accounts',
    # business apps
    'business.inventory',
    'business.products',
    'business.orders',
    'business.payment',
    'business.authorization',
    # client apps
    'client.checkout',
    'client.cart',
    'client.products.apps.ProductsConfig',
    'client.delivery',
    'client.web',
    # utils
    'utils.session'
]
