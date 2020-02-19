from allauth.account import app_settings
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm
from rest_auth.serializers import (
    PasswordResetSerializer as ResetPasswordSerializer,
    UserDetailsSerializer,
    LoginSerializer as BaseLoginSerializer
)
from rest_framework import serializers

from .models import User, UserProfile, StaffUser


class KnoxSerializer(serializers.Serializer):
    """
    Serializer for Knox authentication.
    """
    token = serializers.CharField()
    user = UserDetailsSerializer()


# serializer for logging in a user
class LoginSerializer(BaseLoginSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        user = self._validate_username_email(username, email, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError(msg)

        if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
            email_address, isCreated = user.emailaddress_set.get_or_create(email=user.email)
            if not email_address.verified:
                send_email_confirmation(self.context["request"], user)
                raise serializers.ValidationError('E-mail is not verified.Check your email')
        attrs['user'] = user
        return attrs


# serializer for creating a user
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'second_name'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        None,
                                        validated_data['password'])
        return user


# serializer for changing a password
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'password'
        ]
        # extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        User.objects.get(
            username=validated_data["username"]
        ).set_password(validated_data["new_password"])

    def validate(self, data):
        user = authenticate(
            **{
                "username": data["username"],
                "password": data["current_password"],
            }
        )
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


# serializer for displaying user data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'username'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "user",
            "gender",
            "location",
            "phone_number",
            "image",
            "birth_day",
            "bio_data"
        ]


class ResetPasswordForm(PasswordResetForm):
    def save(self, *args, **kwargs):
        super().save(
            subject_template_name='account_registration/password_reset_subject.txt',
            email_template_name='account_registration/password_reset_email.html',
            html_email_template_name='account_registration/password_reset_email.html'
        )


class PasswordResetSerializer(ResetPasswordSerializer):
    password_reset_form_class = ResetPasswordForm


# serializer for creating a staff
class CreateStaffUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffUser
        fields = (
            'user',
            'departments',
            'staff_type'
        )

    def create(self, validated_data):
        staff = StaffUser.objects.create(
            user=validated_data["user"],
            staff_type=validated_data["staff_type"]
        )
        staff.departments.set(validated_data["departments"])

        return staff
