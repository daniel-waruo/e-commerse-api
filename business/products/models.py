from django.conf import settings
from django.db import models
from django.utils.text import slugify
from djmoney.contrib.exchange.models import convert_money
from djmoney.models.fields import MoneyField
from pyuploadcare.dj.models import ImageField

# Create your models here.
from utils.currency.utils import round_off

BASE_CURRENCY = settings.BASE_CURRENCY


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True, max_length=300)

    class Meta:
        unique_together = ('slug', 'parent',)  # enforcing that there can not be two
        verbose_name_plural = "categories"  # categories under a parent with same
        # slug

    def __str__(self):  # __str__ method elaborated later in
        full_path = [self.name]  # post.  use __unicode__ in place of
        # __str__ if you are using python 2
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])


class Product(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    price = MoneyField(max_digits=14, decimal_places=2, blank=False, null=False)
    discount_price = MoneyField(max_digits=14, decimal_places=2)
    price_base = MoneyField(max_digits=14, decimal_places=2, editable=False)
    slug = models.SlugField(unique=True, null=True)
    description = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now=True)

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


class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name="images")
    image = ImageField()
