from functools import reduce

import django_filters
import graphene
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
from graphene_django.filter import DjangoFilterConnectionField

from business.products.models import Product, Category, ProductImage
from client.products.models import ProductReview
from client.products.types import ProductType, ProductNode, ProductImageType, CategoryType, ProductReviewType


class ProductFilter(django_filters.FilterSet):
    # Do case-insensitive lookups on 'name'
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all(), to_field_name='id')

    class Meta:
        model = Product
        fields = ['id', 'slug']


class Query(object):
    product = graphene.Field(
        ProductType,
        id=graphene.String(),
        slug=graphene.String()
    )

    def resolve_product(self, info, id=None, slug=None):
        try:
            # check if there is an id specified
            if id:
                # get product from product id
                return Product.objects.get(id=id)
            # get product from slug
            return Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            # if there is an exception return None
            return None

    all_products = DjangoFilterConnectionField(
        ProductNode,
        filterset_class=ProductFilter
    )

    product_images = graphene.List(ProductImageType)
    product_image = graphene.Field(ProductImageType)

    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        # return all categories
        return Category.objects.all()

    filter_products = DjangoFilterConnectionField(
        ProductNode,
        filterset_class=ProductFilter,
        categorySlugs=graphene.List(graphene.String),
        category_Ids=graphene.List(graphene.String),
        query=graphene.String()
    )

    def resolve_filter_products(self, info, **kwargs):
        category_ids = kwargs.get("category_Ids")
        category_slugs = kwargs.get("categorySlugs")
        query = kwargs.get("query")
        # initial queryset object
        query_set = Product.objects.all()

        # if categoryIds and query not provided
        if not (category_ids or query or category_slugs):
            return query_set
        # TODO: remove category ids filter as it redndant after fully migrating
        # if categoryIds filter
        if category_ids:
            query_set = query_set.filter(category_id__in=category_ids)

        # if categorySlugs filter
        if category_slugs:
            query_set = query_set.filter(category__slug__in=category_slugs)

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
        # return all product images
        return ProductImage.objects.all()

    """Product Reviews"""
    product_reviews = graphene.List(
        ProductReviewType,
        product_slug=graphene.String()
    )

    def resolve_product_reviews(self, info, **kwargs):
        # get product reviews from slug
        if kwargs.get("product_slug"):
            return ProductReview.objects.filter(product__slug=kwargs.get("product_slug"))
        # return node
        return ProductReview.objects.none()
