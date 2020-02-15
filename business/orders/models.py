import shortuuid
from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField
from shortuuidfield import ShortUUIDField

from business.products.models import Product
from business.payment.models import Receipt
from client.delivery.models import DeliveryInfo

# Create your models here.

ORDER_STATES = (
    ('pending', 'Pending'),
    ('cancelled', 'Cancelled'),
    ('shipping', 'Shipping'),
    ('received', 'Received')
)

shortuuid.set_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"


class Order(models.Model):
    """
    Order
    This is the model used to store the order is officially.
    """
    id = ShortUUIDField(default=shortuuid.uuid(), primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receipt = models.OneToOneField(Receipt, on_delete=models.PROTECT, null=True)
    delivery_info = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    state = models.CharField(choices=ORDER_STATES, max_length=10, default='pending')
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Order"

    def get_payment_status(self):
        if not self.receipt:
            return False
        else:
            return True

    def __str__(self):
        return "Order " + str(self.user) + " " + self.state


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    number = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    price_on_purchase = MoneyField(max_digits=14, decimal_places=2, blank=False, null=False, editable=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.price_on_purchase = self.product.price
        return super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = "Product Order"

    def __str__(self):
        return self.product.name
