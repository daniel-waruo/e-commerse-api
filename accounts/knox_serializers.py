from rest_framework import serializers

# from allauth.account.forms import ResetPasswordForm
from .knox_models import Token


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)
