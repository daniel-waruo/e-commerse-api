
# Application definition

MIDDLEWARE = [
    'django.session.security.SecurityMiddleware',
    'django.contrib.sessions.session.SessionMiddleware',
    'django.session.common.CommonMiddleware',
    'django.session.csrf.CsrfViewMiddleware',
    'django.contrib.auth.session.AuthenticationMiddleware',
    'cart.anonymous_session.middleware.CheckoutSessionMiddleware',
    'django.contrib.messages.session.MessageMiddleware',
    'django.session.clickjacking.XFrameOptionsMiddleware',
]