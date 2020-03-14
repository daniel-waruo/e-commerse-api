from django.conf import settings
from django.db import transaction
from django.db.models import Sum, F
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from business.products.models import Product
from client.cart.errors import NoUserIdOrSessionKeyError, NoProductToDelete, BadConfigError
from .models import CartProduct, Cart

BASE_CURRENCY = settings.BASE_CURRENCY


def get_cart_object(user_id=None, session_key=None):
    if user_id and session_key:
        raise BadConfigError("One should not provide both the user id and session key")
    if user_id:
        cart = Cart.objects.get_or_create(user_id=user_id)
    elif session_key:
        cart = Cart.objects.get_or_create(session_id=session_key)
    else:
        raise NoUserIdOrSessionKeyError
    if isinstance(cart, tuple):
        return cart[0]
    return cart


def get_cart_id(user_id=None, session_key=None):
    if user_id:
        return get_cart_object(user_id=user_id).id
    elif session_key:
        return get_cart_object(session_key=session_key).id
    else:
        raise NoUserIdOrSessionKeyError


def get_cart_from_request(request):
    if request.user.is_authenticated:
        user_session_kwargs = {
            'user_id': request.user.id
        }
    else:
        user_session_kwargs = {
            'session_key': request.anonymous_session.session_key
        }
    return get_cart_object(**user_session_kwargs)


def get_grand_total(user_id=None, session_key=None, cart=None, price_field=None):
    if not cart:
        cart = get_cart_object(user_id, session_key)
    if cart.products.all().exists():
        price_field = price_field or 'price_base'
        total = cart.products.aggregate(
            cart_total=Sum(F("number") * F("product__" + price_field), output_field=MoneyField())
        )["cart_total"]
        return Money(total, BASE_CURRENCY)
    else:
        return Money(0, BASE_CURRENCY)


def get_cart_number(user_id=None, session_key=None):
    cart = get_cart_object(user_id, session_key)
    if cart.products.all().exists():
        return cart.products.aggregate(cart_total=Sum("number"))["cart_total"]
    else:
        return 0


def add_product_to_cart(product_pk, request, product_number=1):
    cart = get_cart_from_request(request)
    # check if there is a product cart matching both product and cart
    if cart.products.filter(product=product_pk).exists():
        # add the number of product cart plus one
        cart_product = cart.products.get(product=product_pk)
        cart_product.number = product_number
        cart_product.save()
        return cart_product
    else:
        # create a whole new product cart and save the number as one
        return CartProduct.objects.create(
            number=product_number,
            product=Product.objects.get(pk=product_pk),
            cart=cart
        )


def remove_product_from_cart(product_pk, request):
    if not product_pk: raise NoProductToDelete("Product PK not provided")
    # get cart from request
    cart = get_cart_from_request(request)
    # get products in cart
    if cart.products.filter(product=product_pk).exists():
        # get cart product
        cart_product = cart.products.get(product=product_pk)
        # delete product
        cart_product.delete()
        return cart_product
    # raise Error
    raise NoProductToDelete("The product id {0} cannot be deleted.".format(product_pk))


def update_product_number(product_pk, product_number, request):
    cart = get_cart_from_request(request)
    if cart.products.filter(product=product_pk):
        cart_product = cart.products.get(product=product_pk)
        cart_product.number = product_number
        cart_product.save()
        return cart_product
    else:
        return remove_product_from_cart(product_pk=product_pk, request=request)


def update_cart(products, request):
    cart = get_cart_from_request(request)

    cart_products = cart.products.select_for_update().filter(cart=cart)

    with transaction.atomic():
        for product in cart_products:
            for item in products:
                # check if the product linked to the cart product is equal to the product in the pk
                if product.product.pk == int(item['pk']):
                    # update the cart product
                    cart.products.filter(product=item['pk']).update(number=item['number'])
