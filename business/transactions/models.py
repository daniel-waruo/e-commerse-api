import uuid
from django.conf import settings
from django.contrib.gis.db import models
from djmoney.models.fields import MoneyField
from utils.session.models import CheckoutSession
from pyuploadcare.dj.models import ImageField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here


class PaymentMethod(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    logo = ImageField()
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return str(self.name)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    payment_method = models.ForeignKey(PaymentMethod, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"

    def __str__(self):
        return str(self.id)


class TransactionUserInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    has_account = models.BooleanField(default=True)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Transaction Information"
        verbose_name_plural = "User Transaction Information"

    def __str__(self):
        return "TRANSACTION " + str(self.transaction.id) + str(self.user)


MPESA_CURRENCIES = (
    ('KES', 'Kenyan shilling'),
    ('UGX', 'Ugandan shilling'),
    ('USD', 'Us Dollar')
)


class MpesaTransaction(models.Model):
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, editable=False)
    transaction_code = models.CharField(max_length=10, null=True, editable=False)
    phone_number = PhoneNumberField()
    amount = MoneyField(max_digits=14, decimal_places=2, currency_choices=MPESA_CURRENCIES, editable=False)

    class Meta:
        verbose_name = "Mpesa Transaction"

    def __str__(self):
        return "MPESA TRANSACTION  " + str(self.id)
