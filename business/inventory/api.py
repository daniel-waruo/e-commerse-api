from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import DjangoModelPermissions

from .models import Product, Supplier
from .serializers import ProductSerializer, SupplierSerializer


# supplier api views
class CreateSupplier(CreateAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SupplierSerializer


# supplier api views
class SupplierApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


class ListSupplierApi(ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


# product api views
class CreateProductApi(CreateAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ProductSerializer


class ProductApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ListProducts(ListAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
