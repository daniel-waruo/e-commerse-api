from django.conf import settings
from django.db import models, transaction
from django.db.models import Sum, F
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from business.products.models import Product
from client.cart.errors import NoProductToDelete
from utils.session.models import AnonymousSession

# Create your models hee
AUTH_USER_MODEL = settings.AUTH_USER_MODEL
BASE_CURRENCY = settings.BASE_CURRENCY

# CHECKOUT STATES
cart_state = (
    ('ac', 'active'),  # The cart is still active
    ('ab', 'abandoned'),  # The cart has not been interacted with for a long time
    ('pr', 'processed'),  # The
)


class CartManager(models.Manager):
    def get_from_request(self, request):
        if request.user.is_authenticated:
            cart = self.get_or_create(user_id=request.user.id)
        else:
            cart = self.get_or_create(
                session_id=request.anonymous_session.session_key
            )
        # check if it is an instance of a tuple created by get or create
        if isinstance(cart, tuple):
            # return cart instance
            return cart[0]
        # if cart is not a tuple return cart instance
        return cart


class Cart(models.Model):
    """ Handle storage and retrieval of user carts

        This is the model used to store the cart before an order is officially made
        It stores the User or Session to refer to the cart.
        TODO:set price to be used as price and not to be used as discount price
        TODO:get a better variable name for price
    """
    # user whom the cart belongs to
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, db_index=True)
    # if the user is not authenticated store the session as the user
    session = models.OneToOneField(AnonymousSession, on_delete=models.CASCADE, null=True, db_index=True)
    # the time the cart was created
    timestamp = models.DateTimeField(auto_now=True)
    # the current state of the cart
    state = models.CharField(max_length=2, null=False, choices=cart_state, default='ac')

    objects = CartManager()

    class Meta:
        verbose_name = 'Cart'

    def __str__(self):
        return "Cart {}".format(self.pk)

    def update_product_number(self, product_pk, product_number=1):
        """ Update quantity in a specific product in the cart"""
        if self.products.filter(product=product_pk).exists():
            cart_product = self.products.get(product=product_pk)
            cart_product.number = product_number
            cart_product.save()
            return cart_product
        # return remove product to handle no existent cases
        # TODO: in future raise no product error
        return self.remove_product(product_pk=product_pk)

    def add_product(self, product_pk, product_number=1):
        """ Adds product to the cart and update the cart product if """
        if self.products.filter(product=product_pk).exists():
            return self.update_product_number(product_pk, product_number)
        return CartProduct.objects.create(
            number=product_number,
            product=Product.objects.get(pk=product_pk),
            cart=self
        )

    def remove_product(self, product_pk):
        # check if product in cart products
        if self.products.filter(product=product_pk).exists():
            # get cart product
            cart_product = self.products.get(product=product_pk)
            # delete product
            cart_product.delete()
            # return a cart product instance
            return cart_product
        # raise Error
        raise NoProductToDelete("The product id {0} cannot be deleted.".format(product_pk))

    def update_cart(self, products: list):
        # get cart products
        cart_products = self.products.select_for_update().filter(cart=self)

        with transaction.atomic():
            for product in cart_products:
                for item in products:
                    # check if the product linked to the cart product is equal to the product in the pk
                    if product.product.pk == int(item['pk']):
                        # update the cart product
                        self.products.filter(product=item['pk']).update(number=item['number'])

    def number_of_products(self):
        # check if products in the cart
        if self.products.all().exists():
            # return the number of products in the cart
            return self.products.aggregate(
                cart_total=Sum("number")
            )["cart_total"]
        return 0

    @property
    def total(self, price_field=None):
        if self.products.all().exists():
            price_field = price_field or 'discount_price'
            total = self.products.aggregate(
                cart_total=Sum(F("number") * F("product__" + price_field), output_field=MoneyField())
            )["cart_total"]
            return Money(total, BASE_CURRENCY)

        return Money(0, BASE_CURRENCY)


class CartProduct(models.Model):
    """
        This is a Product on the cart list
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, db_index=True, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'Cart Product'

    def product_total(self, field='discount_price'):
        return self.number * getattr(self.product, field)

    def base_product_total(self):
        return self.number * self.product.base_price()

    def __str__(self):
        return self.product.name
