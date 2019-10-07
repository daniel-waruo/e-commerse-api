from django.urls import path

from .api import OrderView, CreateOrder

urlpatterns = [
    path('order/<pk>', OrderView.as_view(), name='view_order'),
    path('order/add', CreateOrder.as_view(), name='create_order'),
]
