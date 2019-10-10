from django.conf import settings
from django.db import models
from jsonfield import JSONField


class Receipt(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # stores receipt data
    payment_data = JSONField(blank=True)
    # stores price list
    price_list = JSONField(blank=True)
    total = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        pass

    def __str__(self):
        return "<Receipt owner={} created={}>".format(self.user.username, self.created)
