from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import Product, Supplier
from .serializers import ProductSerializer, SupplierSerializer


# supplier api views
class CreateSupplier(CreateAPIView):
    serializer_class = SupplierSerializer


class SupplierApi(RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


class ListSupplierApi(ListAPIView):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


# product api views
class CreateProductApi(CreateAPIView):
    serializer_class = ProductSerializer


class ProductApi(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ListProducts(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
