import graphene
from graphene_django import DjangoObjectType

from .models import Cart, CartProduct
from .utils import get_cart_object, get_grand_total


# This is configured in the CategoryNode's Meta class (as you can see below)
class CartType(DjangoObjectType):
    class Meta:
        model = Cart

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
        if request.user.is_authenticated:
            user_session_kwargs = {
                'user_id': request.user.id
            }
        else:
            user_session_kwargs = {
                'session_key': request.checkout_session.session_key
            }
        return get_cart_object(**user_session_kwargs)

    def resolve_cart_products(self, info, **kwargs):
        request = info.context
        if request.user.is_authenticated:
            return CartProduct.objects.filter(cart__user_id=request.user.id)
        else:
            return CartProduct.objects.filter(cart__session=request.checkout_session.session_key)
