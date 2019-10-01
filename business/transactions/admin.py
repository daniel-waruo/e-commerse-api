from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.TemporarySessionUserInfo)
admin.site.register(models.Transaction)
admin.site.register(models.TransactionUserInfo)
admin.site.register(models.MpesaTransaction)
admin.site.register(models.PaymentMethod)
