import graphene
from djmoney.models.fields import MoneyField
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from business.products.models import Category
from business.products.models import Product, ProductImage
from .models import ProductReview


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


@convert_django_field.register(MoneyField)
def convert_field(field, registry=None):
    return graphene.String()


# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ProductReviewType(DjangoObjectType):
    class Meta:
        model = ProductReview


class ProductNode(DjangoObjectType):
    pk = graphene.String()

    def resolve_pk(self, info):
        return self.pk

    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        filter_fields = [
            'id',
            'slug',
            'category'
        ]
        interfaces = (relay.Node,)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class ProductImageType(DjangoObjectType):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "product")
