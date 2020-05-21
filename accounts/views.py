import rest_framework
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from allauth.account.utils import complete_signup
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.instagram.views import InstagramOAuth2Adapter
from django.shortcuts import get_object_or_404
from graphene_django.views import GraphQLView
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_auth.registration.views import RegisterView as BaseRegisterView
from rest_auth.views import LoginView as BaseLoginView
from rest_auth.views import PasswordResetView as BasePasswordResetView
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import (AllowAny)
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from accounts.serializers import PasswordResetSerializer
from .serializers import TokenSerializer, LoginSerializer
from .utils import create_knox_token


class LoginView(BaseLoginView):
    """ Enables Login with a username or email and a password """
    serializer_class = LoginSerializer

    def get_response(self):
        """Send authentication token to the client"""
        serializer_class = self.get_response_serializer()
        data = {
            'user': self.user,
            'token': self.token
        }
        serializer = serializer_class(instance=data, context={'request': self.request})
        return Response(serializer.data, status=200)


class RegisterView(BaseRegisterView):
    """Enables registration of users into the system"""

    def get_response_data(self, user):
        """Send authentication data to the client"""
        if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": "Verification e-mail sent."}
        return TokenSerializer({'user': user, 'token': self.token}).data

    def perform_create(self, serializer):
        """Create and instance of the user to the database and perform post registration processed
        These processed include sending activation email and sending of post signup signals
        """
        user = serializer.save(self.request)
        self.token = create_knox_token(self.token_model, user, None)
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None)
        return user


class PasswordResetView(BasePasswordResetView):
    serializer_class = PasswordResetSerializer


class ConfirmEmailView(APIView):
    """ Sends a confirmation email to the user """
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


class SocialLoginView(LoginView):
    serializer_class = SocialLoginSerializer

    def process_login(self):
        get_adapter(self.request).login(self.request, self.user)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class InstagramLogin(SocialLoginView):
    adapter_class = InstagramOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class DRFAuthenticatedGraphQLView(GraphQLView):
    """GRAPH-QL View that utilizes authentication from Django Rest Framework"""
    batch = True

    def parse_body(self, request):
        """ Parses Request Data for use in graph-ql"""
        if isinstance(request, rest_framework.request.Request):
            return request.data
        return super(DRFAuthenticatedGraphQLView, self).parse_body(request)

    @classmethod
    def as_view(cls, *args, **kwargs):
        """ Set DRF attributes in the view """
        view = super(DRFAuthenticatedGraphQLView, cls).as_view(*args, **kwargs)
        view = permission_classes((AllowAny,))(view)
        view = authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)(view)
        view = api_view(["GET", "POST"])(view)
        return view
