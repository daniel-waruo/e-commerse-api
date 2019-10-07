from allauth.account.views import (
    email_verification_sent,
    password_reset_from_key
)
from django.urls import path

urlpatterns = [
    # url for informing the user that the verification in sent
    path("confirm-email/", email_verification_sent, name="account_email_verification_sent"),

    # path("password/change/", password_change, name="account_change_password"),

    # path("password/set/", password_set, name="account_set_password"),
    # path("inactive/", account_inactive, name="account_inactive"),

    # E-mail
    # path("email/", email, name="account_email"),
    # path("password/reset/", password_reset, name="account_reset_password"),
    # path("password/reset/done/$", password_reset_done, name="account_reset_password_done"),
    path("password/reset/key/<uidb36>-<key>/", password_reset_from_key,
         name="account_reset_password_from_key"),
    # path("password/reset/key/done/", password_reset_from_key_done, name="account_reset_password_from_key_done"),
]
