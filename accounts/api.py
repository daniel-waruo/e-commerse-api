from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from django.shortcuts import get_object_or_404
from rest_auth.views import PasswordResetView as BasePasswordResetView
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny
from accounts.serializers import PasswordResetSerializer

from rest_framework.response import Response

from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView

from allauth.account.utils import complete_signup
from allauth.account import app_settings as allauth_settings

from .serializers import KnoxSerializer,LoginSerializer
from .utils import create_knox_token
from rest_framework.authtoken.models import Token

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
            return {"detail": ("Verification e-mail sent.")}
        return KnoxSerializer({'user': user, 'token': self.token}).data
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        self.token = create_knox_token(None, user, None)
        complete_signup(self.request._request, user, allauth_settings.EMAIL_VERIFICATION, None)
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
        emailconfirmation = EmailConfirmationHMAC.from_key(key)
        if not emailconfirmation:
            if queryset is None:
                queryset = EmailConfirmation.objects.all_valid()
                queryset = queryset.select_related("email_address__user")
            emailconfirmation = get_object_or_404(queryset, key=key.lower())
        return emailconfirmation
