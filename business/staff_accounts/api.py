from django.contrib.auth import get_user_model
from rest_auth.registration.views import RegisterView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import DjangoModelPermissions

from accounts.models import StaffUser
from accounts.serializers import CreateStaffUserSerializer
from business.authorization.permissions import IsDepartmentMember


class RegisterStaffUserApi(RegisterView):
    """
    Create a User Whom You want to be a staff
    """
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]

    def get_queryset(self):
        return get_user_model().objects.all()


class RegisterStaff(CreateAPIView):
    """
    register a user in the User Staff Model
    """
    serializer_class = CreateStaffUserSerializer
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]

    def get_queryset(self):
        return StaffUser.objects.all()