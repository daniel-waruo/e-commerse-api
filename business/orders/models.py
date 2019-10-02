import shortuuid
from django.db import models
from shortuuidfield import ShortUUIDField

from business.cms.models import Product
from business.delivery.models import DeliveryInfo

# Create your models here.

ORDER_STATES = (
    ('pend', 'Pending'),
    ('del', 'Processed'),
    ('shipping', 'Shipping'),
    ('received', 'Received')
)

PAYMENT_STATES = (
    (True, 'payment complete'),
    (False, 'payment pending')
)

shortuuid.set_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"


class Order(models.Model):
    id = ShortUUIDField(default=shortuuid.uuid(), primary_key=True, editable=False)
    payment_status = models.BooleanField(default=False, choices=PAYMENT_STATES)
    date_added = models.DateField(auto_now_add=True)
    state = models.CharField(choices=ORDER_STATES, max_length=4, default='init')

    class Meta:
        verbose_name = "Order"

    def __str__(self):
        return "Order " + str(self.pk)


class OrderInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    delivery_info = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Order Information"
        verbose_name_plural = "Order Information"

    def __str__(self):
        return "Order Information " + str(self.order.id)


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    number = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    state = models.CharField(choices=ORDER_STATES, max_length=4, default='init')

    class Meta:
        verbose_name = " Product Order"

    def __str__(self):
        return self.product.name
