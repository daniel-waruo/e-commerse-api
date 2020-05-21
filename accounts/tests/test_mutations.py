from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from knox.models import AuthToken
from rest_framework.test import APIClient

from root.schema import schema

User = get_user_model()


class UserEditTestCase(GraphQLTestCase):
    # Here you need to inject your test case's schema
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphi-ql'

    def setUp(self):
        # create and authenticate a user
        # create a user instance
        self.user = User.objects.create_user(
            username='john',
            email='johndoe@gmail.com',
            password='password'
        )
        # create token for the user and get the string
        token, token_string = AuthToken.objects.create(user=self.user)
        self.token = token
        self.token_string = token_string
        self._client = APIClient()
        # client.force_authenticate(user=self.user)
        self._client.login(username='john',password='password')

    def test_with_authorised_user(self):
        response = self.query(
            '''
            mutation EditUserMutation($firstName:String,$lastName:String,$gender:String) {
                editUserMutation(firstName: $firstName,lastName:$lastName,gender:$gender) {
                    user{
                        id
                        firstName
                        lastName
                        email
                        userprofile{
                            phoneNumber
                            gender
                        }
                    }
                    errors
                }
            }
            ''',
            op_name='editUserMutation',
            variables={
                'firstName': 'john',
                'lastName': 'doe',
                'gender': 'm'
            }
        )
        # This validates the status code and if you get errors
        self.assertEqual(response.status_code, 200, "Request not Successful \n{}".format(response.content))
        # This validate that the data has been updated
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual('john', updated_user.first_name, "First Name was not Updated \n{}".format(response.content))
        self.assertEqual('doe', updated_user.last_name, "Last Name was not Updated \n{}".format(response.content))
        self.assertEqual('m', updated_user.userprofile.gender, "Gender was not Updated \n{}".format(response.content))
