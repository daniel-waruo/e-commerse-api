from django.conf import settings
from django.db import models

from utils.phone_number_field import PhoneNumberField


# create your models here

# class PickUpStation(models.Model):
# TODO:Look For an Appropriate Representation For Location
#    pass
class DeliveryInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    email = models.EmailField()

    class Meta:
        verbose_name = 'Delivery Information'

    def __str__(self):
        return str(self.id)
