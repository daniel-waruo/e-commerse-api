from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from accounts.models import StaffUser
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