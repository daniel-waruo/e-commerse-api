from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, ListCreateAPIView

from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category


class CreateProduct(CreateAPIView):
    serializer_class = ProductSerializer


class ProductView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ListProductApi(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CreateCategory(CreateAPIView):
    serializer_class = CategorySerializer


class CategoryView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ListCategoryApi(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
