from business.authorization.apps import DepartmentAppConfig


class UserManagementConfig(DepartmentAppConfig):
    label = 'staff_accounts'
    name = 'business.staff_accounts'
    verbose_name = "User Management"
