from rest_framework.generics import CreateAPIView, RetrieveAPIView

from .serializers import ProductSerializer, CategorySerializer


class CreateProduct(CreateAPIView):
    serializer_class = ProductSerializer


class CreateCategory(CreateAPIView):
    serializer_class = CategorySerializer


class UpdateProduct(RetrieveAPIView):
    serializer_class = ProductSerializer


class UpdateCategory(RetrieveAPIView):
    serializer_class = CategorySerializer
