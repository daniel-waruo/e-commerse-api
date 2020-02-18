import graphene
from graphene_django import DjangoObjectType

from .models import Cart, CartProduct
from .utils import get_cart_object

# This is configured in the CategoryNode's Meta class (as you can see below)
class CartType(DjangoObjectType):
    class Meta:
        model = Cart


class CartProductType(DjangoObjectType):
    class Meta:
        model = CartProduct


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
