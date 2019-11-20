from django.urls import path

from .api import SetDepartmentStaffPermissions, SetDepartmentManagerPermissions

app_name = 'authorization'

urlpatterns = [
    # product urls
    path('add_roles', SetDepartmentStaffPermissions.as_view(), name='get_permissions'),
    path('add_roles', SetDepartmentStaffPermissions.as_view(), name='add_permissions'),
    path('department-managers/add_departments', SetDepartmentManagerPermissions.as_view(),
         name="department_manager_add_departments")
]
