from rest_framework.reverse import reverse

from utils.tests import TestAuthenticatedUser
from django.contrib.auth.models import Group


class TestGroupManagement(TestAuthenticatedUser):

    def test_add_group(self):
        self.client.login(username="test", password="test")
        url = reverse('authorization:add_group')
        response = self.client.get(url, data={

        })
        self.assertEqual(response.status_code, 201,
                         'Group addition is not Successful.\n'
                         'Expected  Response Code 201, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))
