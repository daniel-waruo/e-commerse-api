from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from business.authorization.utils import validate_permissions, validate_departments, get_user_departments, \
    get_valid_permission_ids, get_department_permission_ids
from .models import Department
from .permissions import IsDepartmentManager, IsGeneralManager
from .serializers import UpdateDepartmentSerializer


class UpdateDepartment(RetrieveUpdateAPIView):
    permission_classes = [IsDepartmentManager, DjangoModelPermissions]
    serializer_class = UpdateDepartmentSerializer
    queryset = Department.objects.all()


class SetDepartmentStaffPermissions(GenericAPIView):
    """
    This view is used to set permissions to users
    It is to be accessed by department managers who are part of the department
    """
    permission_classes = [IsDepartmentManager]
    app_label = 'authorization'

    def get_queryset(self):
        return get_user_model().objects.select_related("staffuser")

    def post(self, request, *args, **kwargs):
        # get user id from request data
        user_id = request.data.get("user", None)
        # get permissions from request data
        permissions = request.data.get("permissions")
        # validate the permissions
        validated_permissions, is_valid = validate_permissions(request.user.id, user_id, permissions)
        if is_valid:
            # get the user from the list of staff users
            user = self.get_queryset().get(id=user_id)
            # set permissions of the user
            user.user_permissions.set(validated_permissions)
            # save data
            user.save()
            # return response with all the information to use in successful response
            return Response(data=request.data, status=status.HTTP_200_OK)
        else:
            # return error response invalid permissions assignment
            return Response(data={
                "permissions": "Invalid Permissions Assignment"
            }, status=status.HTTP_403_FORBIDDEN)

    def get(self, request, *args, **kwargs):
        # get user can be given
        user_id = self.request.data.get("user", None)
        # get permissions valid for the particular user
        user_permission_ids = get_valid_permission_ids(user_id)

        # get the permissions the manager can give within his jurisdiction
        view_user_permission_ids = get_department_permission_ids(
            get_user_departments(self.request.user.id)
        )
        # make sure the permission are within both the user and view user
        # this is an intersection that can only be done on sets
        permissions = list(
            set(user_permission_ids).intersection(view_user_permission_ids)
        )
        print(permissions)
        data = {
            "user_id": user_id,
            "permissions": permissions
        }
        # return response with all the information to use in successful response
        return Response(data=data, status=status.HTTP_200_OK)


class SetDepartmentManagerPermissions(GenericAPIView):
    """
    This view is used to set departments to department managers
    It is to be accessed by general  managers who has access to the department
    """
    permission_classes = [IsGeneralManager]
    # explicitly set the app label to be used in permissions
    app_label = 'authorization'

    def get_queryset(self):
        # get all users in the staff user model
        return get_user_model().objects.select_related("staffuser")

    def get(self, request, *args, **kwargs):
        if self.request.user.has_perm('authorization.manage_department_manager'):
            # get user id from request data
            user_id = self.request.data.get("user", None)

            # get departments valid for the particular user
            departments = get_user_departments(self.request.user.id)
            data = {
                "user_id": user_id,
                "departments": get_valid_permission_ids(user_id)
            }
            # return response with all the information to use in successful response
            return Response(data=data, status=status.HTTP_200_OK)
        return Response(data={
            "detail": "You are not authorized."
        }, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        # get user id from request data
        user_id = request.data.get("user", None)
        # get permissions from request data
        departments = request.data.get("departments")
        # validate the permissions

        if self.request.user.has_perm('authorization.manage_department_manager'):
            validated_departments, is_valid = validate_departments(user_id=self.request.user.id,
                                                                   departments=departments)
            if is_valid:
                # get the user from the list of staff users
                user = self.get_queryset().get(id=user_id)
                # set the departments of the department manager
                user.staffuser.departments.set(validated_departments)
                # return response with all the information to use in successful response
                return Response(data=request.data, status=status.HTTP_200_OK)
            else:
                # return error response invalid permissions assignment
                departments_list = list(
                    map(
                        lambda department: department.__str__(),
                        get_user_departments(self.request.user.id)
                    )
                )
                return Response(data={
                    "departments": "Invalid Departments valid Departments are {}.".format(departments_list),
                },
                    status=status.HTTP_403_FORBIDDEN)
                # return error response invalid permissions assignment
        return Response(data={
            "detail": "You are not authorized."
        }, status=status.HTTP_403_FORBIDDEN)


class SetGeneralManagerPermissions(GenericAPIView):
    """
        This view is used to set departments to department managers
        It is to be accessed by general  managers who has access to the department
        """
    permission_classes = [IsGeneralManager]
    # explicitly set the app label to be used in permissions
    app_label = 'authorization'

    def get_queryset(self):
        # get all users in the staff user model
        return get_user_model().objects.select_related("staffuser")

    def post(self, request, *args, **kwargs):
        # get user id from request data
        user_id = request.data.get("user", None)
        # get permissions from request data
        departments = request.data.get("departments")
        # validate the permissions

        if self.request.user.has_perm('authorization.manage_department_manager'):
            validated_departments, is_valid = validate_departments(user_id=self.request.user.id,
                                                                   departments=departments)
            if is_valid:
                # get the user from the list of staff users
                user = self.get_queryset().get(id=user_id)
                # set the departments of the department manager
                user.staffuser.departments.set(validated_departments)
                # return response with all the information to use in successful response
                return Response(data=request.data, status=status.HTTP_200_OK)
            else:
                # return error response invalid permissions assignment
                departments_list = list(
                    map(
                        lambda department: department.__str__(),
                        get_user_departments(self.request.user.id)
                    )
                )
                return Response(data={
                    "departments": "Invalid Departments valid Departments are {}.".format(departments_list),
                },
                    status=status.HTTP_403_FORBIDDEN)
                # return error response invalid permissions assignment
        return Response(data={
            "detail": "You are not authorized."
        }, status=status.HTTP_403_FORBIDDEN)
