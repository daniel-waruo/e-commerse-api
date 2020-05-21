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
            'gender': 'm'
        }
        self.serializer = UserEditSerializer(instance=self.user, data=self.data)

    def test_update_user(self):
        if self.serializer.is_valid():
            user = self.serializer.save()
            self.assertEqual(user.first_name, self.data['first_name'])
            self.assertEqual(user.last_name, self.data['last_name'])
            self.assertEqual(user.userprofile.gender, self.data['gender'])
