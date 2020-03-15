from django.urls import path

from .views import (
    SetDepartmentStaffPermissions,
    SetDepartmentManagerPermissions,
    SetGeneralManagerPermissions)

app_name = 'authorization'

urlpatterns = [
    # department staff url
    path('department-staff', SetDepartmentStaffPermissions.as_view(), name='department-staff'),
    # department-manager url
    path('department-manager', SetDepartmentManagerPermissions.as_view(), name='department-manager'),
    # general manager url
    path('general-manager', SetGeneralManagerPermissions.as_view(), name='general-manager')
]
