from django.urls import path
from rest_auth.views import (
    LogoutView,
    UserDetailsView,
    PasswordChangeView,
    PasswordResetConfirmView,
    # PasswordResetView,
)

from accounts.api import PasswordResetView,KnoxLoginView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('login/', KnoxLoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change')
]
