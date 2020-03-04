import os

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    # 'http://localhost:3000',
]
if os.environ.get('FRONT_END_URLS'):
    urls = os.environ.get('FRONT_END_URLS')
    urls = urls.split("+")
    CORS_ORIGIN_WHITELIST += urls

CORS_ALLOW_CREDENTIALS = True
