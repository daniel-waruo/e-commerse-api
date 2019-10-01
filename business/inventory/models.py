import uuid

from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Write your models here

User = settings.AUTH_USER_MODEL
BASE_CURRENCY = settings.BASE_CURRENCY


class Supplier(models.Model):
    name = models.CharField(null=False)
    identifier = models.CharField(unique=True)

    def __str__(self):
        return self.identifier


class Contacts(models.Model):
    supplier = models.OneToOneField(to=Supplier, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        pass


class Shipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        pass


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    weight = models.DecimalField(max_digits=20, decimal_places=2)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Product, self).save(*args, **kwargs)

    def weight_str(self):
        return str(self.weight)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product design"
