from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers

from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ['number', 'product']


class CartSerializer(serializers.ModelSerializer):
    products = CartProductSerializer(many=True, source='product_set', read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'session']

    def validate(self, data):
        if not (data['user'] or data['session']):
            raise ImproperlyConfigured("Either the User or Session must be specified")
        super().validate(data)
