from rest_framework.reverse import reverse

from business.authorization.utils import get_valid_permission_ids, get_all_department_ids
from utils.tests import TestStaffSuperUser, unsuccessful_message


class TestSetStaffRoles(TestStaffSuperUser):
    def test_get_department_staff_permissions(self):
        url = reverse("authorization:get_permissions")
        user = self.create_user()
        self.create_staff_user(user_id=user.id)
        response = self.client.get(url, data={
            "user": user.id
        }, format='json')
        self.assertEqual(
            response.status_code, 200,
            unsuccessful_message(
                response, "Get Roles Valid to Departmental Staff", 200))

    def test_set_department_staff_permissions(self):
        url = reverse("authorization:add_permissions")
        user = self.create_user()
        self.create_staff_user(user_id=user.id)
        response = self.client.post(url, data={
            "user": user.id,
            "permissions": get_valid_permission_ids(user_id=user.id)
        }, format='json')
        self.assertEqual(
            response.status_code, 200,
            unsuccessful_message(
                response, "Add Roles to Departmental Staff", 200))

    def test_set_department_manager_departments(self):
        url = reverse("authorization:department_manager_add_departments")
        user = self.create_user()
        staff = self.create_staff_user(user_id=user.id)
        response = self.client.post(url, data={
            "user": user.id,
            "departments": get_all_department_ids(),
        }, format='json')

        self.assertEqual(response.status_code, 200,
                         'Add Departments to Manager is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))
