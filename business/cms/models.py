from django.db import models
from business.inventory.models import Product as BaseProduct
from djmoney.models.fields import MoneyField
from django.db import models
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from pyuploadcare.dj.models import ImageField
from django.conf import settings
# Create your models here.
from utils.currency.utils import round_off
from django.db.models.signals import post_save
from django.utils.text import slugify

MyUser = settings.AUTH_USER_MODEL
BASE_CURRENCY = settings.BASE_CURRENCY


class Product(models.Model):
    product = models.OneToOneField(to=BaseProduct, on_delete=models.CASCADE)
    price = MoneyField(max_digits=14, decimal_places=2)
    discount_price = MoneyField(max_digits=14, decimal_places=2)
    timestamp = models.DateTimeField(auto_now=True)
    price_base = MoneyField(max_digits=14, decimal_places=2, editable=False)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.price_base = convert_money(self.price, BASE_CURRENCY)
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def base_price(self):
        m = convert_money(self.price, BASE_CURRENCY)
        return round_off(m)

    def __str__(self):
        return self.name
