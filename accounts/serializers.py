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

from .models import User, StaffUser, gender_choices, UserProfile


class TokenSerializer(serializers.Serializer):
    """
      Serializer for Knox library authentication authentication.
    """
    token = serializers.CharField()
    user = UserDetailsSerializer()


# serializer for logging in a user
class LoginSerializer(BaseLoginSerializer):
    """
    Login
    Serializer for handling login in our application
    it inherits from Login Serializer and is tweaked for
    login using Knox library
    """

    def validate(self, attrs):
        # get data
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        # check whether the user credentials are valid
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
            email_address, _ = user.emailaddress_set.get_or_create(email=user.email)
            if not email_address.verified:
                send_email_confirmation(self.context["request"], user)
                raise serializers.ValidationError('E-mail is not verified.Check your email')
        attrs['user'] = user
        return attrs


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


class UserEditSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    gender = serializers.ChoiceField(choices=gender_choices, required=False)
    phone_number = PhoneNumberField(required=False)

    def validate(self, data):
        if not self.instance:
            raise serializers.ValidationError("Instance Must be Provided")
        return data

    def validate_phone_number(self, value):
        """Check if the phone number belongs to another user"""
        user_profile = self.context.user.userprofile
        if UserProfile.objects.filter(phone_number=value) and (user_profile.phone_number != value):
            raise Exception(
                "Phone Number belong to another user"
            )
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
