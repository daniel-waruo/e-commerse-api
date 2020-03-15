from django.urls import path

from .views import RegisterStaffUserApi, RegisterStaff

app_name = 'staff_accounts'

urlpatterns = [
    # product urls
    path('register-user', RegisterStaffUserApi.as_view(), name='add_user'),
    path('register-user-staff', RegisterStaff.as_view(), name='add_user_staff'),
]
