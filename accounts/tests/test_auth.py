from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from knox.models import AuthToken

from ..auth import TokenAuthentication


# models test
class TokenAuthTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get("/")

        # create a user instance
        self.user = get_user_model().objects.create_user(
            username='john',
            email='johndoe@gmail.com',
            password='password'
        )
        # create token for the user and get the string
        token, token_string = AuthToken.objects.create(user=self.user)
        self.token = token
        self.token_string = token_string

    @staticmethod
    def set_header(request, token_string):
        request.META = {
            **request.META,
            "HTTP_AUTHORIZATION": "Token {}".format(token_string)
        }
        return request

    def test_token_authentication(self):
        request = self.set_header(self.request, self.token_string)
        # get authentication object
        authentication_object = TokenAuthentication().authenticate(request)
        # assert that the authentication object is not None
        self.assertIsNotNone(authentication_object, "Token Authentication Failed")

    def test_invalid_token(self):
        request = self.set_header(self.request, "FaketokenString")
        # get authentication object
        authentication_object = TokenAuthentication().authenticate(request)
        # assert that the authentication object is not None
        self.assertIsNone(authentication_object, "Token Authentication Failed")
