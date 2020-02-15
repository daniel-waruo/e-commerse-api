from django.urls import path
from .api import CreateCategory, CreateProduct, ProductView, CategoryView, ListCategoryApi, ListProductApi

app_name = 'cms'

urlpatterns = [
    # product urls
    path('products/product/add', CreateProduct.as_view(), name='add_product'),
    path('products/product/<int:pk>', ProductView.as_view(), name='product_view'),
    path('products', ListProductApi.as_view(), name='list_products'),
    # category urls
    path('categories/category/add', CreateCategory.as_view(), name='add_category'),
    path('categories/category/<int:pk>', CategoryView.as_view(), name='category_view'),
    path('categories', ListCategoryApi.as_view(), name='list_categories'),
]
