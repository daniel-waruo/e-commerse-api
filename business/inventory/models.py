import uuid

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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
SIZE_CATEGORY = (
    (1, 'Small'),
    (2, 'Medium'),
    (3, 'Large')
)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    supplier = models.ManyToManyField(to=Supplier)
    weight = models.DecimalField(max_digits=20, decimal_places=2)
    size = models.PositiveSmallIntegerField(default=1)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super(Product, self).save(*args, **kwargs)

    def weight_str(self):
        return str(self.weight)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "product inventory"
