import graphene

from business.products.models import Product, Category, ProductImage
from client.products.models import ProductReview
from client.products.types import ProductType, ProductImageType, CategoryType, ProductReviewType, \
    FilterProducts
from .utils import filter_products


class Query(object):
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
        query=graphene.String()
    )

    def resolve_filter_products(self, info, **kwargs):
        return FilterProducts(
            products=filter_products(kwargs)
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
