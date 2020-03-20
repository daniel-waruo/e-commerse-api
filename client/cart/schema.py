import graphene
from graphene_django import DjangoObjectType

from .models import Cart, CartProduct


# This is configured in the CategoryNode's Meta class (as you can see below)
class CartType(DjangoObjectType):
    class Meta:
        model = Cart

    number = graphene.Int()

    def resolve_number(self: Cart, info):
        return self.number_of_products()

    total = graphene.String()

    def resolve_total(self: Cart, info):
        return self.total


class CartProductType(DjangoObjectType):
    total = graphene.String()

    class Meta:
        model = CartProduct

    def resolve_total(self: CartProduct, info):
        return self.number * self.product.discount_price


class Query(graphene.ObjectType):
    cart = graphene.Field(CartType)
    cart_products = graphene.List(CartProductType)

    def resolve_cart(self, info):
        request = info.context
        # get and return cart object type
        return Cart.objects.get_from_request(request)

    def resolve_cart_products(self, info, **kwargs):
        request = info.context
        if request.user.is_authenticated:
            return CartProduct.objects.filter(cart__user_id=request.user.id)
        else:
            return CartProduct.objects.filter(cart__session=request.anonymous_session.session_key)
