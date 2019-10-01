from allauth.account.models import EmailConfirmationHMAC, EmailConfirmation
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_auth.views import PasswordResetView as BasePasswordResetView
from accounts.serializers import PasswordResetSerializer


class PasswordResetView(BasePasswordResetView):
    serializer_class = PasswordResetSerializer


class ConfirmEmailApi(APIView):

    def post(self, *args, **kwargs):
        key = kwargs.get("key")
        confirmation = self.get_confirmation_object(key)
        if not confirmation.email_address.verified:
            confirmation.confirm(self.request)
            return Response({
                "detail": "Email Verification successful"
            })
        else:
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
