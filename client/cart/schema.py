import graphene
from graphene_django import DjangoObjectType

from .models import Cart, CartProduct
from .utils import get_grand_total, get_cart_from_request


# This is configured in the CategoryNode's Meta class (as you can see below)
class CartType(DjangoObjectType):
    class Meta:
        model = Cart

    number = graphene.Int()

    resolve_number = ''
    total = graphene.String()

    def resolve_total(self, info):
        return get_grand_total(cart=self, price_field="discount_price")


class CartProductType(DjangoObjectType):
    total = graphene.String()

    class Meta:
        model = CartProduct

    def resolve_total(self, info):
        return self.number * self.product.discount_price


class Query(object):
    cart = graphene.Field(CartType)
    cart_products = graphene.List(CartProductType)

    def resolve_cart(self, info):
        request = info.context
        return get_cart_from_request(request)

    def resolve_cart_products(self, info, **kwargs):
        request = info.context
        if request.user.is_authenticated:
            return CartProduct.objects.filter(cart__user_id=request.user.id)
        else:
            return CartProduct.objects.filter(cart__session=request.anonymous_session.session_key)
