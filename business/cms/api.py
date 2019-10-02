from rest_framework.generics import CreateAPIView

from .serializers import ProductSerializer, CategorySerializer


class CreateProduct(CreateAPIView):
    serializer_class = ProductSerializer


class CreateCategory(CreateAPIView):
    serializer_class = CategorySerializer
