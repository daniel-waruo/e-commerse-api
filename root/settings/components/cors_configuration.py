import os

CORS_ORIGIN_ALLOW_ALL = False

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]
if os.environ.get('FRONT_END_URL'):
    CORS_ORIGIN_WHITELIST.append(os.environ.get('FRONT_END_URL'))

CORS_ALLOW_CREDENTIALS = True
