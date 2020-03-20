from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from allauth.account.utils import complete_signup
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from django.shortcuts import get_object_or_404
from rest_auth.helpers import complete_social_signup
from rest_auth.registration.serializers import (SocialLoginSerializer)
from rest_auth.registration.views import RegisterView, SocialRegisterView
from rest_auth.views import LoginView
from rest_auth.views import PasswordResetView as BasePasswordResetView
from rest_framework.permissions import (AllowAny)
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers import PasswordResetSerializer
from .serializers import KnoxSerializer, LoginSerializer
from .utils import create_knox_token


class KnoxLoginView(LoginView):
    serializer_class = LoginSerializer

    def get_response(self):
        serializer_class = self.get_response_serializer()

        data = {
            'user': self.user,
            'token': self.token
        }
        serializer = serializer_class(instance=data, context={'request': self.request})

        return Response(serializer.data, status=200)


class KnoxRegisterView(RegisterView):

    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": "Verification e-mail sent."}
        return KnoxSerializer({'user': user, 'token': self.token}).data

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None)
        return user


class KnoxSocialRegisterView(SocialRegisterView):
    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": "Verification e-mail sent."}
        return KnoxSerializer({'user': user, 'token': self.token}).data

    def perform_create(self, serializer):
        self.request.session.pop('socialaccount_sociallogin', None)
        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        complete_social_signup(self.request, self.sociallogin)
        return user


class PasswordResetView(BasePasswordResetView):
    serializer_class = PasswordResetSerializer


class ConfirmEmailApi(APIView):
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        key = kwargs.get("key")
        confirmation = self.get_confirmation_object(key)
        if not confirmation.email_address.verified:
            confirmation.confirm(self.request)
            return Response({
                "detail": "Email Verification successful"
            })

        return Response({
            "detail": "Your Email was already verified.Try logging in."
        })

    @staticmethod
    def get_confirmation_object(key, queryset=None):
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = EmailConfirmation.objects.all_valid()
                queryset = queryset.select_related("email_address__user")
            email_confirmation = get_object_or_404(queryset, key=key.lower())
        return email_confirmation


class SocialLoginView(KnoxLoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class InstagramLogin(SocialLoginView):
    adapter_class = InstagramOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
