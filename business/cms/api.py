from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import DjangoModelPermissions

from business.authorization.permissions import IsDepartmentMember
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class CreateProduct(CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = ProductSerializer


class ProductView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ListProductApi(ListAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CreateCategory(CreateAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ListCategoryApi(ListAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
