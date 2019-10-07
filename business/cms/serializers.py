from rest_framework.serializers import ModelSerializer
from .models import Product, Category


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['product', 'name', 'images', 'category', 'price', 'discount_price', 'slug', 'description',
                  'timestamp']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'id']
