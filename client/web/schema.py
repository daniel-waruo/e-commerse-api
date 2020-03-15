import graphene
from graphene_django import DjangoObjectType

from .models import CarouselItem, FeaturedProduct


class CarouselType(DjangoObjectType):
    class Meta:
        model = CarouselItem


class FeaturedProductType(DjangoObjectType):
    class Meta:
        model = FeaturedProduct


class Query(graphene.ObjectType):
    all_carousel = graphene.List(CarouselType)
    all_featured_products = graphene.List(FeaturedProductType)

    def resolve_all_carousel(self, info, **kwargs):
        return CarouselItem.objects.all()

    def resolve_all_featured_products(self, info, **kwargs):
        return FeaturedProduct.objects.all()
