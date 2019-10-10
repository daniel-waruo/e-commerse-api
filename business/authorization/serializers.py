from rest_framework.serializers import ModelSerializer
from .models import Department


class UpdateDepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

    def save(self, **kwargs):
        return self.update(**kwargs)
