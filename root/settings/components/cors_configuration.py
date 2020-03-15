import os

from corsheaders.defaults import default_headers

CORS_ALLOW_HEADERS = list(default_headers) + [
    'anonymous-session',
]

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = []

if os.environ.get('FRONT_END_URLS'):
    urls = os.environ.get('FRONT_END_URLS')
    urls = urls.split("+")
    CORS_ORIGIN_WHITELIST += urls

CORS_ALLOW_CREDENTIALS = True
