from rest_framework import serializers

from .models import Product, Category, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['product',
                  'name',
                  'category',
                  'price', 'price_currency',
                  'discount_price', 'discount_price_currency',
                  'slug',
                  'description',
                  'timestamp']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'id']
