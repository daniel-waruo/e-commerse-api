from rest_framework import serializers

from .models import *


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['number', 'product']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='product_set', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'payment_status', 'state']
