from allauth.account import app_settings
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from phonenumber_field.serializerfields import PhoneNumberField
from rest_auth.serializers import (
    PasswordResetSerializer as ResetPasswordSerializer,
    UserDetailsSerializer,
    LoginSerializer as BaseLoginSerializer
)
from rest_framework import serializers

from .models import User, gender_choices, UserProfile


class TokenSerializer(serializers.Serializer):
    """
      Serializer for Knox library authentication authentication.
    """
    token = serializers.CharField()
    user = UserDetailsSerializer()

    def create(self, validated_data):
        """TODO:Implement abstract create method"""
        pass

    def update(self, instance, validated_data):
        """TODO:Implement abstract update method"""
        pass


# serializer for logging in a user
class LoginSerializer(BaseLoginSerializer):
    """ Serializer for handling password authentication """

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        # check whether the provides user credentials are valid
        user = self._validate_username_email(username, email, password)
        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg)
        # send a confirmation email if email verification is mandatory and the user has not yet confirmed the email
        if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            email_address, _ = user.emailaddress_set.get_or_create(email=user.email)
            if not email_address.verified:
                send_email_confirmation(self.context["request"], user)
                raise serializers.ValidationError('E-mail is not verified.Check your email')
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


# serializer for changing a password
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password'
        ]

    def create(self, validated_data):
        user = User.objects.get(username=validated_data["username"])
        user.set_password(validated_data["new_password"])
        user.save()
        return user

    def validate(self, data):
        user = authenticate(**{"username": data["username"], "password": data["current_password"]})
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class ResetPasswordForm(PasswordResetForm):
    """ Override default email templates """

    def save(self, *args, **kwargs):
        super().save(
            subject_template_name='account_registration/password_reset_subject.txt',
            email_template_name='account_registration/password_reset_email.html',
            html_email_template_name='account_registration/password_reset_email.html'
        )


class PasswordResetSerializer(ResetPasswordSerializer):
    """Override password_reset_form_class with out custom one above """
    password_reset_form_class = ResetPasswordForm


class UserEditSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = PhoneNumberField(required=False)
    gender = serializers.ChoiceField(choices=gender_choices, required=False)

    def validate(self, data):
        if not self.instance:
            raise serializers.ValidationError("User instance not available for editing")
        return data

    def validate_phone_number(self, value):
        """Check if the phone number belongs to another user"""
        user_profile = self.instance.userprofile
        if UserProfile.objects.filter(phone_number=value) and (user_profile.phone_number != value):
            raise serializers.ValidationError("Phone Number belong to another user.Hence is not available")
        return value

    def update(self, user, validated_data):
        """ Update user data  in the database """
        user.first_name = validated_data.get('first_name') or user.first_name
        user.last_name = validated_data.get('last_name') or user.last_name
        user.userprofile.phone_number = validated_data.get('phone_number') or user.userprofile.phone_number
        user.userprofile.gender = validated_data.get('gender') or user.userprofile.gender
        user.save()
        user.userprofile.save()
        return user

    def save(self):
        user = self.update(self.instance, self.validated_data)
        return user

    def create(self, validated_data):
        pass
