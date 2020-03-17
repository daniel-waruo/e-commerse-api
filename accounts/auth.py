from knox.auth import TokenAuthentication as BaseTokenAuth

try:
    from hmac import compare_digest
except ImportError:
    def compare_digest(a, b):
        return a == b

import binascii

from rest_framework import exceptions
from rest_framework.authentication import (
    get_authorization_header,
)

from knox.crypto import hash_token
from knox.models import AuthToken
from knox.settings import CONSTANTS, knox_settings


class TokenAuthentication(BaseTokenAuth):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        prefix = knox_settings.AUTH_HEADER_PREFIX.encode()

        if not auth or auth[0].lower() != prefix.lower():
            return None
        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            return None

        elif len(auth) > 2:
            msg = 'Invalid token header. ' \
                  'Token string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)
        try:
            user, auth_token = self.authenticate_credentials(auth[1])
        except TypeError:
            return None
        return user, auth_token

    def authenticate_credentials(self, token):
        '''
        Due to the random nature of hashing a salted value, this must inspect
        each auth_token individually to find the correct one.

        Tokens that have expired will be deleted and skipped
        '''
        token = token.decode("utf-8")
        for auth_token in AuthToken.objects.filter(
                token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH]):
            if self._cleanup_token(auth_token):
                continue

            try:
                digest = hash_token(token, auth_token.salt)
            except (TypeError, binascii.Error):
                return None
            if compare_digest(digest, auth_token.digest):
                if knox_settings.AUTO_REFRESH and auth_token.expiry:
                    self.renew_token(auth_token)
                return self.validate_user(auth_token)
        return None
