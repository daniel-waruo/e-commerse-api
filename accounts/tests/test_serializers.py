from django.contrib.auth import get_user_model
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sites.models import Site
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from accounts.serializers import UserEditSerializer, ChangePasswordSerializer, LoginSerializer

User = get_user_model()


class UserEditSerializerTestCase(TestCase):

    def setUp(self):
        # create and authenticate a user
        self.user = User.objects.create_user(
            username='john',
            email='johndoe@gmail.com',
            password='password'
        )
        self.data = {
            'first_name': 'Daniel',
            'last_name': 'Waruo',
            'gender': 'm',
            'phone_number': '+254722485461'
        }
        self.serializer = UserEditSerializer(instance=self.user, data=self.data)

    def test_update_user(self):
        if self.serializer.is_valid():
            user = self.serializer.save()
            self.assertEqual(user.first_name, self.data['first_name'])
            self.assertEqual(user.last_name, self.data['last_name'])
            self.assertEqual(user.userprofile.gender, self.data['gender'])
            self.assertEqual(user.userprofile.phone_number, self.data['phone_number'])


class ChangePasswordSerializerTestCase(TestCase):
    def setUp(self):
        # create and authenticate a user
        self.user = User.objects.create_user(
            username='john',
            email='johndoe@gmail.com',
            password='password'
        )
        self.data = {
            'username': 'john',
            'current_password': 'password',
            'new_password': 'new-password'
        }
        self.serializer_class = ChangePasswordSerializer
        self.serializer = self.serializer_class(data=self.data)

    def test_wrong_credentials_on_password(self):
        """ Test to check whether wrong credentials can change a user password """
        data = {
            'username': 'john',
            'current_password': 'password-wrong',
            'new_password': 'new-password'
        }
        serializer = self.serializer_class(data=data)
        # make sure the data is false
        self.assertFalse(serializer.is_valid(), "Wrong Credentials not flagged")

    def test_change_password(self):
        """ Test whether a user can change their password """
        if self.serializer.is_valid():
            user = self.serializer.save()
            self.assertEqual(user.password, self.data['new_password'])


class LoginSerializerTestCase(TestCase):
    def setUp(self):
        """ create a user """
        self.user = User.objects.create_user(
            username='john',
            email='johndoe@gmail.com',
            password='password'
        )
        # create a a site for that will bear the HTTP_HOST header
        Site.objects.create(domain='testing.com', name='Testing Domain')

        request = APIRequestFactory().get('rest_login', HTTP_HOST='testing.com')
        # in your test method:
        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()

        self.serializer_class = LoginSerializer
        self.context = {'request': request}

    def test_unverified_email_user_login(self):
        data = {'username': 'john', 'password': 'password'}
        self.serializer = self.serializer_class(data=data, context=self.context)
        self.assertFalse(self.serializer.is_valid(), "Error in data validation \n")

    def _verify_email_address(self):
        # manually confirm the users email address
        from allauth.account.models import EmailAddress
        EmailAddress.objects.get_or_create({
            'user': self.user,
            'email': self.user.email,
            'verified': True,
            'primary': True,
        }, user=self.user)

    def test_verified_email_user_login(self):
        self._verify_email_address()
        data = {'username': 'john', 'password': 'password'}
        self.serializer = self.serializer_class(data=data, context=self.context)
        self.assertTrue(self.serializer.is_valid(), "Error in data validation \n")

    def test_wrong_credentials_user_login(self):
        self._verify_email_address()
        data = {'username': 'john', 'password': 'wrong-password'}
        self.serializer = self.serializer_class(data=data, context=self.context)
        self.assertFalse(self.serializer.is_valid(), "Security Threat wrong password authenticates.")
