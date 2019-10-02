from rest_framework.serializers import ModelSerializer
from .models import DeliveryInfo


class DeliveryInfoSerializer(ModelSerializer):
    class Meta:
        model = DeliveryInfo
        fields = [
            'user',
            'phone_number',
            'email'
        ]
