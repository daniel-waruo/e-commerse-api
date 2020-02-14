from django.conf import settings
from django.db import models

from business.products.models import Product
from utils.session.models import CheckoutSession

# Create your models hee
AUTH_USER_MODEL = settings.AUTH_USER_MODEL

# CHECKOUT STATES
cart_state = (
    ('ac', 'active'),  # The cart is still active
    ('ab', 'abandoned'),  # The cart has not been interacted with for a long time
    ('pr', 'processed'),  # The
)


class Cart(models.Model):
    """
    Cart
    This is the model used to store the cart before an order is officially made
    It stores the User or Session to refer to the cart.
    """
    # user whom the cart belongs to
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, db_index=True)
    # if the user is not authenticated store the session as the user
    session = models.OneToOneField(CheckoutSession, on_delete=models.CASCADE, null=True, db_index=True)
    # the time the cart was created
    timestamp = models.DateTimeField(auto_now=True)
    # the current state of the cart
    state = models.CharField(max_length=2, null=False, choices=cart_state, default='ac')

    class Meta:
        verbose_name = 'Cart'

    def __str__(self):
        return "Cart " + str(self.pk)


class CartProduct(models.Model):
    """
        This is a Product on the cart list
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, db_index=True,related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'Cart Product'

    def product_total(self):
        return self.number * self.product.price

    def base_product_total(self):
        return self.number * self.product.base_price()

    def __str__(self):
        return self.product.name
