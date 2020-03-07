from django.conf import settings
from django.db import models

from business.products.models import Product

AUTH_USER = settings.AUTH_USER_MODEL

rating_choices = (
    (1, 'One'),
    (2, 'Two'),
    (3, 'Three'),
    (4, 'Four'),
    (5, 'Five')
)


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(AUTH_USER, on_delete=models.CASCADE, related_name='reviews')
    rating = models.SmallIntegerField(choices=rating_choices)
    text = models.TextField()

    class Meta:
        unique_together = ['product', 'user']
