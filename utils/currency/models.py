from django.contrib.gis.db import models
from djmoney.models import fields
from djmoney.settings import CURRENCY_CHOICES


# Create your models here.


class Currency(models.Model):
    currency_code = fields.CurrencyField(choices=CURRENCY_CHOICES, unique=True)
    name = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        if not str(self.name):
            return str(self.currency_code)
        else:
            return str(self.name)
