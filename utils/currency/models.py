from django.contrib.gis.db import models
from django.contrib.postgres.fields import (
    JSONField,
    ArrayField)
from djmoney.settings import CURRENCY_CHOICES
from djmoney.models.fields import CurrencyField


# Create your models here.


class Currency(models.Model):
    currency_code = CurrencyField(choices=CURRENCY_CHOICES, unique=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        if not str(self.name):
            return str(self.currency_code)
        else:
            return str(self.name)
