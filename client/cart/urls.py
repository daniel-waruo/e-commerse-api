from django.urls import path, include
from .api import *

urlpatterns = [
    # cart related urls
    path('product/add', AddProduct.as_view(), name='cart_add_product'),
    path('product/remove', RemoveProduct.as_view(), name='cart_remove_product'),
    path('product/add_number', AddProductNumber.as_view(), name='cart_add_product_number'),
    path('product/subtract_number', SubtractProductNumber.as_view(), name='cart_subtract_product_number'),
    path('product/update_number', UpdateProductNumber.as_view(), name='cart_update_product_number')
]
