from rest_framework.serializers import ModelSerializer
from .models import Product, Supplier


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'weight', 'supplier', 'size']


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'identifier', 'name', 'phone_number', 'email']
