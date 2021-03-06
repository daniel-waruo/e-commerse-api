from django.urls import path

from .views import (
    AddProduct,
    RemoveProduct,
    UpdateProductNumber,
    UpdateCart
)

app_name = 'cart'

urlpatterns = [
    # cart related urls
    path('product/add', AddProduct.as_view(), name='cart_add_product'),
    path('product/remove', RemoveProduct.as_view(), name='cart_remove_product'),
    path('product/update_number', UpdateProductNumber.as_view(), name='cart_update_product_number'),
    path('update', UpdateCart.as_view(), name='cart_update')
]
