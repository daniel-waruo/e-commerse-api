from django.db import models
from business.products.models import Product

class CarouselItem(models.Model):
    title = models.CharField(max_length=100)
    caption = models.TextField()
    url_to = models.URLField()
    image_url = models.URLField()

    def __str__(self):
        return self.title

class FeaturedProduct(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

