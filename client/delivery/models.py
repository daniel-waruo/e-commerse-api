from django.conf import settings
from django.db import models

from utils.phone_number_field import PhoneNumberField


class DeliveryInfo(models.Model):
    """ Contains Delivery information for people to be delivered to

    TODO:change name from Delivery Info to Delivery Contacts
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='delivery_contacts')
    phone_number = PhoneNumberField()
    email = models.EmailField()
    contact_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Delivery Information'

    def __str__(self):
        return str(self.id)

# TODO: add a model to store previous delivery location in form of coordinates
