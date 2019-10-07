from rest_framework.serializers import ModelSerializer

from .models import Product, Category


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['product',
                  'name',
                  'images',
                  'category',
                  'price', 'price_currency',
                  'discount_price', 'discount_price_currency',
                  'slug',
                  'description',
                  'timestamp']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'id']
