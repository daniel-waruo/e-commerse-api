from functools import reduce

import django_filters
import graphene
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from djmoney.models.fields import MoneyField
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphene_django.filter import DjangoFilterConnectionField
from pyuploadcare.dj.models import ImageField

from business.products.models import Category, Product, ProductImage
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


class ProductFilter(django_filters.FilterSet):
    # Do case-insensitive lookups on 'name'
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), to_field_name='id')

    class Meta:
        model = Product
        fields = ['id', 'slug']


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


class Query(object):
    product = graphene.Field(ProductType, id=graphene.String(), slug=graphene.String())
    all_products = DjangoFilterConnectionField(ProductNode, filterset_class=ProductFilter)

    filter_products = DjangoFilterConnectionField(ProductNode,
                                                  filterset_class=ProductFilter,
                                                  categorySlugs=graphene.List(graphene.String),
                                                  category_Ids=graphene.List(graphene.String),
                                                  query=graphene.String()
                                                  )

    product_images = graphene.List(ProductImageType)
    product_image = graphene.Field(ProductImageType)

    all_categories = graphene.List(CategoryType)

    product_reviews = graphene.List(ProductReviewType,
                                    product_slug=graphene.String())

    def resolve_product(self, info, id=None, slug=None):
        try:
            if id:
                return Product.objects.get(id=id)
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return None

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_filter_products(self, info, **kwargs):
        categoryIds = kwargs.get("category_Ids")
        categorySlugs = kwargs.get("categorySlugs")
        query = kwargs.get("query")
        # initial queryset object
        query_set = Product.objects.all()

        # if categoryIds and query not provided
        if not (categoryIds or query or categorySlugs):
            return query_set
        # TODO: remove category ids filter as it redndant after fully migrating
        # if categoryIds filter
        if categoryIds:
            query_set = query_set.filter(category_id__in=categoryIds)

        # if categorySlugs filter
        if categorySlugs:
            query_set = query_set.filter(category__slug__in=categorySlugs)

        # if query filter according to the query
        if query:
            # get the list of search queries
            queries = map(lambda x: SearchQuery(x), query.split())
            # get the reduced search queries using the or
            queries_or = reduce(lambda a, b: a | b, queries)
            # get the search vector
            vector = SearchVector('name', weight='A') + \
                     SearchVector('description', weight='B') + \
                     SearchVector('category__name', weight='C')

            # set search rank
            rank = SearchRank(vector, queries_or)
            query_set = query_set.annotate(
                rank=rank
            ).order_by('-rank')

        # return query set
        return query_set

    def resolve_product_images(self, info, **kwargs):
        return ProductImage.objects.all()

    def resolve_product_reviews(self, info, **kwargs):
        if kwargs.get("product_slug"):
            return ProductReview.objects.filter(product__slug=kwargs.get("product_slug"))
        return ProductReview.objects.none()
