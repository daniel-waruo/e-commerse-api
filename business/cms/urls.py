from django.urls import path
from .api import CreateCategory, CreateProduct, UpdateCategory, UpdateProduct

urlpatterns = [
    path('products/create/', CreateProduct.as_view(), name='create_product'),
    path('category/create/', CreateCategory.as_view(), name='create_category'),
    path('products/update/<int:pk>', UpdateProduct.as_view(), name='update_product'),
    path('category/update/<int:pk>', UpdateCategory.as_view(), name='update_category'),
]
