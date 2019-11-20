# Create your tests here.
from rest_framework.reverse import reverse

from business.authorization.utils import get_all_department_ids
from utils.tests import TestStaffSuperUser


class TestStaffAccounts(TestStaffSuperUser):

    def test_create_staff_user(self):
        # permissions
        url = reverse("staff_accounts:add_user")
        response = self.client.post(url, data={
            'username': "test-username",
            'email': "test@gmail.com",
            'password1': 'test-password',
            'password2': 'test-password',

        })
        self.assertEqual(response.status_code, 201,
                         'Staff User not Created.Expected Response Code 201, received {0} instead.'
                         'It returned {1}'
                         .format(response.status_code, response.content))

    def test_create_staff_model_entry(self):
        # permissions
        url = reverse("staff_accounts:add_user_staff")
        user = self.create_user()
        departments = get_all_department_ids()[:2]
        response = self.client.post(url, data={
            "user": user.id,
            "departments": departments,
            "staff_type": 1,
        }, format='json')
        self.assertEqual(response.status_code, 201,
                         'Staff User not Created.Expected Response Code 201, received {0} instead.'
                         'It returned {1}'
                         .format(response.status_code, response.content))
