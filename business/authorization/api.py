from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import DjangoModelPermissions
from .serializers import UpdateDepartmentSerializer
from .models import Department


class UpdateDepartment(RetrieveUpdateAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = UpdateDepartmentSerializer
    queryset = Department.objects.all()

