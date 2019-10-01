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


def get_cart_object(user_id=None, session_key=None):
    if user_id:
        if Cart.objects.filter(user=user_id).exists():
            return Cart.objects.get(user=user_id)
        else:
            return None
    elif session_key:
        if Cart.objects.filter(session_id=session_key).exists():
            return Cart.objects.get(session_id=session_key)
        else:
            return None
    else:
        raise NoUserIdOrSessionKeyError


# Create your views here.
def get_cart_id(user_id=None, session_key=None):
    if user_id:
        if get_cart_object(user_id=user_id):
            return get_cart_object(user_id=user_id).id
    elif session_key:
        if get_cart_object(session_key=session_key):
            return get_cart_object(session_key=session_key).id
    else:
        raise NoUserIdOrSessionKeyError


def get_grand_total(cart_id):
    if CartProduct.objects.filter(cart=cart_id).exists():
        total = CartProduct.objects.filter(
            cart=cart_id
        ).aggregate(
            cart_total=Sum(F("number") * F("product__price_base"), output_field=MoneyField())
        )["cart_total"]
        return Money(total, BASE_CURRENCY)
    else:
        return Money(0, BASE_CURRENCY)


def get_cart_number(user_id=None, session_key=None):
    if user_id:
        if Cart.objects.filter(user=user_id).exists():
            cart = Cart.objects.get(user=user_id)
            if cart.cartproduct_set.all().exists():
                return cart.cartproduct_set.aggregate(cart_total=Sum("number"))["cart_total"]
            else:
                return 0
        else:
            return 0
    elif session_key:
        if Cart.objects.filter(session_id=session_key).exists():
            cart = Cart.objects.get(session_id=session_key)
            if cart.cartproduct_set.all().exists():
                return cart.cartproduct_set.aggregate(cart_total=Sum("number"))["cart_total"]
            else:
                return 0
        else:
            return 0
    else:
        raise NoUserIdOrSessionKeyError


def add_product_to_cart(product_pk, user_id=None, session_key=None):
    cart_product = None
    if user_id:
        # check for existence of cart model linked to user
        if Cart.objects.filter(user=user_id).exists():
            # get the cart object
            cart = get_cart_object(user_id=user_id)
            # check if there is a product cart matching both product and cart
            if cart.cartproduct_set.filter(product=product_pk).exists():
                # add the number of product cart plus one
                cart_product = cart.cartproduct_set.get(product=product_pk)
                cart_product.number += 1
                cart_product.save()
            else:
                # create a whole new product cart and save the number as one
                CartProduct.objects.create(
                    number=1,
                    product=Product.objects.get(pk=product_pk),
                    cart=cart
                )
        else:
            # create a new cart and add one product cart the number as one
            cart = Cart.objects.create(
                user_id=user_id
            )
            # create a new cart
            CartProduct.objects.create(
                number=1,
                product=Product.objects.get(pk=product_pk),
                cart=cart,
            )
    elif session_key:
        # if no user_id use anonymous_session key for anonymous users
        # check availability of cart
        if Cart.objects.filter(session_id=session_key).exists():
            cart = Cart.objects.get(session_id=session_key)
            if cart.cartproduct_set.filter(product=product_pk).exists():
                # add the number of product cart plus one
                cart_product = cart.productcart_set.get(product=product_pk)
                cart_product.number += 1
                cart_product.save()
            else:
                # create a whole new product cart and save the number as one
                cart_product = CartProduct(
                    number=1,
                    product=Product.objects.get(pk=product_pk),
                    cart=cart
                )
                cart_product.save()
        else:
            # create a new cart and add one product cart the number as one
            from utils.session.models import CheckoutSession
            session = CheckoutSession.objects.get(session_key=session_key)
            cart = Cart(session=session)
            cart.save()
            # create a new cart
            cart_product = CartProduct(
                number=1,
                product=Product.objects.get(pk=product_pk),
                cart=cart,
            )
            cart_product.save()
    else:
        raise NoUserIdOrSessionKeyError
    return cart_product


class NoProductToDelete(Exception):
    pass


def remove_product_from_cart(product_pk, user_id=None, session_key=None):
    if not product_pk:
        raise Exception(product_pk)
    if user_id:
        if Cart.objects.filter(user=user_id).exists():
            cart = Cart.objects.get(user=user_id)
            if cart.cartproduct_set.filter(product=product_pk).exists():
                cart_product = cart.cartproduct_set.get(product=product_pk)
                cart_product.delete()
            else:
                raise NoProductToDelete("The user id " + str(user_id) + "has no product cart")
        else:
            raise NoProductToDelete("There is no cart for user id " + str(user_id))
    elif session_key:
        if Cart.objects.filter(session_id=session_key).exists():
            cart = Cart.objects.get(session_id=session_key)
            if cart.cartproduct_set.filter(product=product_pk).exists():
                cart_product = cart.productcart_set.get(product=product_pk)
                cart_product.delete()
            else:
                raise NoProductToDelete("The session has no product cart")
        else:
            raise NoProductToDelete("There is no cart for this session")
    else:
        raise NoUserIdOrSessionKeyError("no user id or cart given")


def add_product_number(product_pk, user_id=None, session_key=None):
    if user_id:
        if Cart.objects.filter(user=user_id).exists():
            cart = Cart.objects.get(user=user_id)
            if cart.objects.filter(cart=cart.id, product=product_pk):
                cart_product = CartProduct.objects.get(cart=cart.id, product=product_pk)
                cart_product.number += 1
                cart_product.save()
                return cart_product
            else:
                return add_product_to_cart(product_pk=product_pk, user_id=user_id)
        else:
            return add_product_to_cart(product_pk=product_pk, user_id=user_id)
    elif session_key:
        if Cart.objects.filter(session_id=session_key).exists():
            cart = Cart.objects.get(session_id=session_key)
            if cart.cartproduct_set.filter(product=product_pk):
                cart_product = cart.cartproduct_set.get(product=product_pk)
                cart_product.number += 1
                cart_product.save()
                return cart_product
            else:
                return add_product_to_cart(product_pk=product_pk, session_key=session_key)
        else:
            return add_product_to_cart(product_pk=product_pk, session_key=session_key)
    else:
        raise NoUserIdOrSessionKeyError


def subtract_product_number(product_pk, user_id=None, session_key=None):
    if user_id:
        if Cart.objects.filter(user=user_id).exists():
            cart = Cart.objects.get(user=user_id)
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
        else:
            return remove_product_from_cart(product_pk, user_id=user_id)
    elif session_key:
        if Cart.objects.filter(session_id=session_key).exists():
            cart = Cart.objects.get(session_id=session_key)
            if cart.cartproduct_set.filter(product=product_pk):
                cart_product = cart.cartproduct_set.get(product=product_pk)
                if cart_product.number > 0:
                    cart_product.number -= 1
                    cart_product.save()
                    return cart_product
                else:
                    return remove_product_from_cart(product_pk=product_pk, session_key=session_key)
            else:
                return remove_product_from_cart(product_pk=product_pk, session_key=session_key)
        else:
            return remove_product_from_cart(product_pk=product_pk, session_key=session_key)
    else:
        raise NoUserIdOrSessionKeyError


def change_product_number(cart_product_id, product_number):
    cart_product = CartProduct.objects.get(pk=cart_product_id)
    cart_product.number = product_number
    cart_product.save()
    return cart_product
