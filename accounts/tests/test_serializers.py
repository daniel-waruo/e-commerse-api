from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.serializers import UserEditSerializer

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
        self.serializer_class = UserEditSerializer
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
