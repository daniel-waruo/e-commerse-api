from django.db import models

"""
The department should not be autogenerated 
-create a department
-link it to the apps dealing with those departments
-restrict access to the api-endpoints based on whether a user is allowed to access the end points 
"""


class Department(models.Model):
    """
    Department are a generic way  of limiting access to certain apps
    """
    app_label = models.CharField(max_length=100, editable=False)
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = 'Department'
        permissions = (
            # permission held by staff_account department users
            ('add_staff', "Can add staff to a department"),
            # department_manager permissions and general manager perms
            ('set_permissions', "Set permissions of a Departmental staff"),
            ('include_department', "Add a department to a staff's access"),
            # general manager permissions
            ('manage_department_manager', "Manage the access of a Departmental Manager"),
            # super user permissions
            ('edit_departments', "Can edit the name of a Department"),
            ('manage_general_manager', "Manage the access of a General Manager"),
        )

    def save(self, *args, **kwargs):
        if kwargs.get("name", None):
            self.name = kwargs.get("name")
        elif not kwargs.get("name", None):
            if not self.name:
                self.name = self.app_label
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name + " Department"
