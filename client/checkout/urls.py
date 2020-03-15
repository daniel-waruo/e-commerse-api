from django.urls import path

from .views import CheckoutApi

app_name = "checkout"

urlpatterns = [
    # cart related urls
    path('', CheckoutApi.as_view(), name='checkout'),
]
