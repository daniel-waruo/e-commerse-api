from allauth.account.views import (
    email_verification_sent,
    password_reset_from_key
)
from django.urls import path

urlpatterns = [
    # url for informing the user that the verification in sent
    path("confirm-email/", email_verification_sent, name="account_email_verification_sent"),
    # url for handling reser key
    path("password/reset/key/<uidb36>-<key>/",
         password_reset_from_key,
         name="account_reset_password_from_key"),
]
