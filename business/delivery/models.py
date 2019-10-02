import uuid
from django.conf import settings
from django.db import models
from utils.geo.phone_numbers.fields import PhoneNumberField


# create your models here


class DeliveryInfo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = PhoneNumberField()
    email = models.EmailField(default="none@gmail.com")

    class Meta:
        verbose_name = 'Checkout User Info'

    def __str__(self):
        return str(self.id)
