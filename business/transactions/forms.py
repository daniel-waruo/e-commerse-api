import inspect
import sys
from django import forms
from . import models
from transactionsapp.africastalking import AfricasTalking
from django.urls import reverse
africastalking = AfricasTalking()


class MpesaTransactionForm(forms.ModelForm):
    payment_method = "mpesa"
    form_url = '/transaction/phone_transaction'

    class Meta:
        model = models.MpesaTransaction
        fields = [
            'phone_number',
        ]

    def get_form_url(self):
        return reverse("transactions:phone_transaction")

    def get_payment_method(self):
        return models.PaymentMethod.objects.get(pk=self.payment_method)

    def pay(self, money):
        phone_number = self.cleaned_data.get("phone_number")
        response = africastalking.mobile_checkout(phone_number, money)
        return response


class TransactionUserInfoForm(forms.ModelForm):
    class Meta:
        model = models.TemporarySessionUserInfo
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]


PAYMENT_FORMS = []


for class_ in inspect.getmembers(sys.modules[__name__], inspect.isclass):
    if hasattr(class_[1], "payment_method"):
        PAYMENT_FORMS.append(class_[1])
