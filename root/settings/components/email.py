import os

# email specifications
SEND_GRID_API_KEY = os.environ.get("SEND_GRID_API_KEY")
# EMAIL_HOST = 'smtp.sendgrid.com'
# EMAIL_HOST_USER = env("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
