import uuid

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from business.products.models import Product


# Write your models here


class Supplier(models.Model):
    name = models.CharField(max_length=100, null=False)
    identifier = models.CharField(max_length=100, unique=True)
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.identifier


class Shipment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4())
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Shipment ' + str(self.id)


"""
TODO:
    - Implement JSON Field
"""

measured_in = (
    ("weight", "Sold per Weight"),
    ("unit", "Sold per Unit")
)


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    supplier = models.ManyToManyField(to=Supplier)
    measured_in = models.BooleanField()
    number = models.PositiveIntegerField(default=0)

    def in_stock(self):
        if self.number == 0:
            return False
        return True

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = "product inventory"
