from allauth.account.views import email_verification_sent
from django.urls import path
from rest_auth.registration.views import RegisterView, VerifyEmailView

from accounts.api import ConfirmEmailApi

urlpatterns = [
    # url for registering new users
    path('', RegisterView.as_view(), name='rest_register'),
    # url for verifying email
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    # url for account confirmation
    path('account-confirm-email/<str:key>', ConfirmEmailApi.as_view(), name='account_confirm_email'),
    # url for informing the user that the verification in sent
    path("confirm-email/", email_verification_sent, name="account_email_verification_sent"),
]
