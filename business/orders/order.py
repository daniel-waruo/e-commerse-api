import datetime

from checkout.models import Checkout, ProductCheckout
from checkout.models import CheckoutFlow
from checkout.utils import get_grand_total
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
# Create your views here.
from django.template.loader import render_to_string
from django.utils import timezone
from front_end.template_names import template_
from ordersapp.models import Order as MyOrder, ProductOrder, OrderInfo
from transactionsapp.africastalking import AfricasTalking
from transactionsapp.models import Transaction, MpesaTransaction

africastalking = AfricasTalking()


class Order:

    def __init__(self, mobile_transaction_data: dict = None, user=None):
        """
        Parameters
        mobile_transaction_data:dict
            {
                "phonenumber": phonenumber:str,
                "amount": Amount of Money:decimal,
                "email": Email :str,
                "first_name": first_name :str,
                "last_name": last_name:str
            }
        """
        self.date = timezone.now()
        self.payment_method = mobile_transaction_data["payment_method"]
        self.user = user
        self.checkout = Checkout.objects.get(user=self.user.id)
        self.amount = get_grand_total(checkout_id=self.checkout.id)
        checkout_flow = CheckoutFlow.objects.get(checkout=self.checkout)
        self.user_info = checkout_flow.address_info

    def date_due(self):
        return self.date + datetime.timedelta(days=7)

    def make_mobile_transaction(self):
        phone_number = self.user_info.phone_number
        transaction = Transaction(
            payment_method=self.payment_method
        )
        # make transaction information
        transaction.save()
        mpesatransaction = MpesaTransaction(
            transaction=transaction,
            phonenumber=phone_number,
            amount=self.amount
        )
        mpesatransaction.save()
        return transaction

    def checkout_to_order(self):
        transaction = self.make_mobile_transaction()
        # create an order
        order = MyOrder(
            transaction=transaction,
            date_due=self.date_due()
        )
        order.save()
        order_info = OrderInfo(
            order=order,
            order_info=self.user_info
        )
        order_info.save()
        # save the order
        #  get the checkout linked to the user
        # get all the products in the checkout
        checkout_products = ProductCheckout.objects.filter(checkout=self.checkout.pk)
        # use the info in checkout product to order product
        for product in checkout_products:
            product_order = ProductOrder(product=product.product,
                                         number=product.number,
                                         order=order)
            product_order.save()
        self.checkout.delete()
        return order

    def order_confirmation_context(self):
        order = self.checkout_to_order()
        context = {
            'user': self.user,
            'order': order,
            'order_products': ProductOrder.objects.filter(order=order.id),
        }
        return context

    def send_email_order_confirmation(self, context):
        email = self.user_info.email
        subject = "PRODUCTS RECEIPT"
        to = [email]
        from_email = settings.DEFAULT_FROM_EMAIL
        message = get_template(template_["order_confirmation"]).render(context)
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    def send_message_order_confirmation(self, context):
        context["total_amount"] = self.amount
        response = africastalking.send_one_sms(
            message=render_to_string(template_["order_message_confirm"], context=context),
            recipient=self.user_info.phone_number,
        )
        return response

    def send_email_message_confirmation(self):
        context = self.order_confirmation_context()
        self.send_email_order_confirmation(context)
        self.send_message_order_confirmation(context)

    def create(self):
        self.send_email_message_confirmation()
