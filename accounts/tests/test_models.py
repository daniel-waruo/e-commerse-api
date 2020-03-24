from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory


# models test
class UserProfileTest(TestCase):
    """
    Test whether user profile is created after user creation
    """
    def setUp(self):
        # Every test needs access to the request factory.
        self.request = RequestFactory().get("/")

        # create a user instance
        self.user = get_user_model().objects.create_user(
            username='john',
            email='johndoe@gmail.com',
            password='password'
        )

    def test_create_userprofile(self):
        # t
        self.assertIsNotNone(self.user.userprofile)
