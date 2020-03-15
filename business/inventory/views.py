from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import DjangoModelPermissions

from business.authorization.permissions import IsDepartmentMember
from .models import Product, Supplier
from .serializers import ProductSerializer, SupplierSerializer


# supplier api views
class CreateSupplier(CreateAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


# supplier api views
class SupplierApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


class ListSupplierApi(ListAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.all()


# product api views
class CreateProductApi(CreateAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ListProducts(ListAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
