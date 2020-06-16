import shortuuid
from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField
from shortuuidfield import ShortUUIDField
# local imports
from business.payment.models import Receipt
from business.products.models import Product
from client.delivery.models import DeliveryInfo
# import SendyIT API wrapper
from sendy_it import SendyIT, Person, Location, Delivery, DeliveryItem
from client.cart.models import Cart

# initialize sendy
sendy = SendyIT(
    settings.SENDY_API_KEY,
    settings.SENDY_USERNAME
)

shortuuid.set_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0987654321"


class OrderManager(models.Manager):
    """Order Manager """

    def create_from_cart(self, cart: Cart, delivery_info: DeliveryInfo, sendy_order_no=None):
        order = self.create(user=cart.user, delivery_info=delivery_info)
        cart_products = cart.products.all()

        def cart_to_order(cart_product):
            ProductOrder.objects.create(
                product=cart_product.product,
                number=cart_product.number,
                order=order,
                price_on_purchase=cart_product.product.discount_price
            )

        # convert the cart products to order products
        map(cart_to_order, cart_products)

        # create a sendy delivery if the order no is provided
        if sendy_order_no:
            SendyDeliveryInfo.objects.create(
                order=order,
                sendy_order_no=sendy_order_no
            )
        # delete the cart then return the order
        cart.delete()
        return order


class Order(models.Model):
    ORDER_STATES = (
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('shipping', 'Shipping'),
        ('received', 'Received')
    )
    """ Order creating and managements"""
    id = ShortUUIDField(default=shortuuid.uuid(), primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receipt = models.OneToOneField(Receipt, on_delete=models.PROTECT, null=True)
    delivery_info = models.ForeignKey(DeliveryInfo, on_delete=models.CASCADE)
    state = models.CharField(choices=ORDER_STATES, max_length=10, default='pending')
    date_added = models.DateField(auto_now_add=True)

    objects = OrderManager()

    class Meta:
        verbose_name = "Order"

    def get_payment_status(self):
        """check whether the order has been paid"""
        return bool(self.receipt)

    def get_order_delivery_details(self, **kwargs):
        """Get Order Products and convert them into delivery items"""
        # convert product order to delivery item
        delivery_items = list(map(
            lambda product: DeliveryItem(
                name=product.product.name
            ),
            self.products.all()
        ))
        return Delivery(
            items=delivery_items,
            **kwargs
        )

    def request_delivery(self, to_location: Location, from_location: Location, sender: Person, recipient: Person,
                         quote=True):
        """Request Delivery From Sendy IT"""
        # TODO:include details for number of products and their
        # height weight weight and name of good
        # key word arguments
        kwargs = dict(
            to_location=to_location,
            from_location=from_location,
            sender=sender,
            recipient=recipient,
            delivery_details=self.get_order_delivery_details()
        )
        if quote:
            response_data = sendy.get_delivery_quote(**kwargs)
            self.state = 'pending'
        else:
            self.state = 'shipping'
            response_data = sendy.make_delivery(**kwargs)
        # save the new state of the delivery
        self.save()
        # get order no from response data
        sendy_order_no = response_data['data']['order_no']
        # create a Sendy Info Instance or Update it if it is there
        if self.sendy_info:
            self.sendy_info.sendy_order_no = sendy_order_no
            self.sendy_info.save()
        else:
            SendyDeliveryInfo.objects.create(
                order=self,
                sendy_order_no=sendy_order_no
            )
        return response_data

    def cancel_order(self):
        """ Cancels the order """
        order_no = self.sendy_info.sendy_order_no
        self.state = 'cancelled'
        self.save()
        return sendy.cancel_delivery(order_no)

    def complete_order(self):
        """ Completes the  Order after getting delivery Rates """
        order_no = self.sendy_info.sendy_order_no
        self.state = 'shipping'
        self.save()
        return sendy.complete_delivery(order_no)

    def __str__(self):
        return "Order " + str(self.user) + " " + self.state


class SendyDeliveryInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='sendy_info')
    sendy_order_no = models.CharField(max_length=255)

    def __str__(self):
        return "SENDY-{}".format(self.sendy_order_no)


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='products')
    price_on_purchase = MoneyField(max_digits=14, decimal_places=2, blank=False, null=False, editable=False)
    number = models.PositiveIntegerField(default=1)

    def save(self, **kwargs):
        self.price_on_purchase = self.product.price
        return super().save(**kwargs)

    class Meta:
        verbose_name = "Product Order"

    def __str__(self):
        return self.product.name
