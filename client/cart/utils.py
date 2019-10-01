from django.db.models import Sum, F
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from django.conf import settings
from business.cms.models import Product
from .models import CartProduct, Cart

BASE_CURRENCY = settings.BASE_CURRENCY


class NoUserIdOrSessionKeyError(Exception):
    pass


class NoCart(Exception):
    pass


class BadConfigError(Exception):
    pass


def get_cart_object(user_id=None, session_key=None):
    if user_id and session_key:
        raise BadConfigError("One should not provide both the user id and session key")
    if user_id:
        return Cart.objects.get_or_create(user=user_id)
    elif session_key:
        return Cart.objects.get_or_create(session_id=session_key)
    else:
        raise NoUserIdOrSessionKeyError


def get_cart_id(user_id=None, session_key=None):
    if user_id:
        return get_cart_object(user_id=user_id).id
    elif session_key:
        return get_cart_object(session_key=session_key).id
    else:
        raise NoUserIdOrSessionKeyError


def get_grand_total(user_id=None, session_key=None):
    cart = get_cart_object(user_id, session_key)
    if cart.cartproduct_set.all().exists():
        total = cart.cartproduct_set.filter.aggregate(
            cart_total=Sum(F("number") * F("product__price_base"), output_field=MoneyField())
        )["cart_total"]
        return Money(total, BASE_CURRENCY)
    else:
        return Money(0, BASE_CURRENCY)


def get_cart_number(user_id=None, session_key=None):
    cart = get_cart_object(user_id, session_key)
    if cart.cartproduct_set.all().exists():
        return cart.cartproduct_set.aggregate(cart_total=Sum("number"))["cart_total"]
    else:
        return 0


def add_product_to_cart(product_pk, user_id=None, session_key=None):
    cart = get_cart_object(user_id=user_id, session_key=session_key)
    # check if there is a product cart matching both product and cart
    if cart.cartproduct_set.filter(product=product_pk).exists():
        # add the number of product cart plus one
        cart_product = cart.cartproduct_set.get(product=product_pk)
        cart_product.number += 1
        cart_product.save()
        return cart_product
    else:
        # create a whole new product cart and save the number as one
        return CartProduct.objects.create(
            number=1,
            product=Product.objects.get(pk=product_pk),
            cart=cart
        )


class NoProductToDelete(Exception):
    pass


def remove_product_from_cart(product_pk, user_id=None, session_key=None):
    cart = get_cart_object(user_id, session_key)
    if cart.cartproduct_set.filter(product=product_pk).exists():
        cart_product = cart.cartproduct_set.get(product=product_pk)
        cart_product.delete()
        return cart_product
    else:
        raise NoProductToDelete("The user id " + str(user_id) + "has no product cart")


def add_product_number(product_pk, user_id=None, session_key=None):
    cart = get_cart_object(user_id, session_key)
    if cart.objects.filter(cart=cart.id, product=product_pk):
        cart_product = CartProduct.objects.get(cart=cart.id, product=product_pk)
        cart_product.number += 1
        cart_product.save()
        return cart_product
    else:
        return add_product_to_cart(product_pk=product_pk, user_id=user_id)


def subtract_product_number(product_pk, user_id=None, session_key=None):
    cart = get_cart_object(user_id, session_key)
    if cart.cartproduct_set.filter(product=product_pk):
        cart_product = cart.cartproduct_set.get(product=product_pk)
        if cart_product.number > 0:
            cart_product.number -= 1
            cart_product.save()
            return cart_product
        else:
            return remove_product_from_cart(product_pk=product_pk, user_id=user_id)
    else:
        return remove_product_from_cart(product_pk=product_pk, user_id=user_id)


def change_product_number(cart_product_id, product_number):
    cart_product = CartProduct.objects.get(pk=cart_product_id)
    cart_product.number = product_number
    cart_product.save()
    return cart_product


class CartDetails:
    def __init__(self, user_id=None, session=None):
        self.total_number = get_cart_number(user_id, session)
        self.total_value = get_grand_total(user_id, session)
