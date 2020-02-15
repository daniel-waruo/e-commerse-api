
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('accounts.auth.TokenAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

REST_AUTH_TOKEN_MODEL = 'knox.models.AuthToken'
REST_AUTH_TOKEN_CREATOR = 'accounts.utils.create_knox_token'

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'accounts.serializers.UserDetailsSerializer',
    'TOKEN_SERIALIZER': 'accounts.serializers.KnoxSerializer',
}