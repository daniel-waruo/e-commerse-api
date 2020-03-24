""" e_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import (
    password_reset_from_key,
    email_verification_sent
)
from django.urls import path
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetConfirmView
)

from .views import (
    KnoxRegisterView, ConfirmEmailApi,
    PasswordResetView, KnoxLoginView,
    FacebookLogin, InstagramLogin, GoogleLogin
)

urlpatterns = [
    ###########################
    # REGISTRATION URLS
    ###########################
    path('registration/', KnoxRegisterView.as_view(), name='rest_register'),
    # url for verifying email
    path('registration/verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    # url for account confirmation
    path('registration/account-confirm-email/<str:key>', ConfirmEmailApi.as_view(), name='account_confirm_email'),
    # url for informing the user that the verification in sent
    path("registration/confirm-email/", email_verification_sent, name="account_email_verification_sent"),

    ###########################
    # AUTHENTICATION URLS
    ###########################
    path('login/', KnoxLoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view(), name='rest_logout'),

    ###########################
    # PASSWORD HANDLING URLS
    ###########################
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path(
        "password/reset/key/<uidb36>-<key>/",
        password_reset_from_key,
        name="account_reset_password_from_key"
    ),

    ###########################
    # SOCIAL LOGIN URLS
    ###########################
    path('social/instagram/', InstagramLogin.as_view(), name='ig_login'),
    path('social/google/', GoogleLogin.as_view(), name='g_login'),
    path('social/facebook/', FacebookLogin.as_view(), name='fb_login')
]
