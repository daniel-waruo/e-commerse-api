from django.urls import path
from .api import (
    CreateProductApi,
    ProductApi,
    ListProducts,
    CreateSupplier,
    SupplierApi,
    ListSupplierApi,
)

app_name = 'inventory'

urlpatterns = [
    path('products/product/add', CreateProductApi.as_view(), name='add_product'),
    path('products/product/<int:pk>', ProductApi.as_view(), name='product_view'),
    path('products', ListProducts.as_view(), name='list_products'),
    path('suppliers/supplier/add', CreateSupplier.as_view(), name='add_supplier'),
    path('suppliers/supplier/<pk>', SupplierApi.as_view(), name='supplier_view'),
    path('suppliers', ListSupplierApi.as_view(), name='list_suppliers'),
]
