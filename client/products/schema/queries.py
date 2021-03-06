import graphene

from business.products.models import Product, Category, ProductImage
from client.products.models import ProductReview
from client.products.schema.types import (
    ProductType,
    ProductImageType,
    CategoryType,
    ProductReviewType,
    FilterProducts
)
from client.products.utils import filter_products, filter_by_price


class Query(graphene.ObjectType):
    """ Product Query"""
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

    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        # return all categories
        return Category.objects.all()

    """Filter Products"""
    filter_products = graphene.Field(
        FilterProducts,
        categorySlugs=graphene.List(graphene.String),
        category_Ids=graphene.List(graphene.String),
        query=graphene.String(),
        min=graphene.String(),
        max=graphene.String()
    )

    def resolve_filter_products(self, info, **kwargs):
        category_slug = kwargs.get("categorySlugs")
        if category_slug:
            category_slug = category_slug[0]

        category = None
        if category_slug:
            if Category.objects.filter(slug=category_slug).exists():
                category = Category.objects.get(slug=category_slug)
        # filter by category query
        all_products = filter_products(kwargs)
        # filter by price
        query_set = filter_by_price(all_products, kwargs)
        return FilterProducts(
            all_products=all_products,
            products=query_set,
            category=category
        )

    """Product Images"""
    product_images = graphene.List(ProductImageType)

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
