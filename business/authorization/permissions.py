from rest_framework.permissions import IsAuthenticated

from accounts.models import StaffUser
from business.authorization.models import Department


class IsStaff(IsAuthenticated):
    """
    Allows access only to admin users.
    """

    def is_staff(self, user):
        if StaffUser.objects.filter(user=user):
            self.staff_user = StaffUser.objects.get(user=user)
            return True
        else:
            return False

    def has_permission(self, request, view):
        if super().has_permission(request, view):
            if self.is_staff(request.user):
                return True
        return False


class IsDepartmentMember(IsStaff):
    """
    To pass this test the user must be in the same department as the current view.

    """

    def get_department(self, app_label=None, model_cls=None):
        """
        Given a model return the department in which it belongs
        """
        if not app_label:
            app_label = model_cls._meta.app_label
        if Department.objects.filter(app_label=app_label):
            if Department.objects.filter(app_label=app_label).count() == 1:
                return Department.objects.get(app_label=app_label)
        return None

    def _queryset(self, view):
        assert hasattr(view, 'get_queryset') \
               or getattr(view, 'queryset', None) is not None, (
            'Cannot apply {} on a view that does not set '
            '`.queryset` or have a `.get_queryset()` method or does not have an app_label attr.'
        ).format(self.__class__.__name__)

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
            assert queryset is not None, (
                '{}.get_queryset() returned None'.format(view.__class__.__name__)
            )
            return queryset
        return view.queryset

    def has_permission(self, request, view):
        # get the app label of current app label of the view
        if hasattr(view, "app_label"):
            if self.get_department(app_label=getattr(view, "app_label")):
                department = self.get_department(app_label=getattr(view, "app_label"))
            else:
                raise AttributeError('The app_label for the view {0} is None'.format(view.__class__.__name__))
        else:
            queryset = self._queryset(view)
            department = self.get_department(model_cls=queryset.model)
        if super().has_permission(request, view):
            assert self.staff_user
            departments = self.staff_user.departments.all()
            if department in departments:
                return True
            elif request.user.is_superuser:
                return True
        return False


class IsDepartmentManager(IsDepartmentMember):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            assert self.staff_user
            if self.staff_user.staff_type >= 1:
                return True
        return False


class IsGeneralManager(IsDepartmentMember):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            assert self.staff_user
            if self.staff_user.staff_type >= 2:
                return True
        return False
