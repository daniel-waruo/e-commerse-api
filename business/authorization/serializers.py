from rest_framework.serializers import ModelSerializer

from .models import Department


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class UpdateDepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

    def save(self, **kwargs):
        return self.update(**kwargs)
