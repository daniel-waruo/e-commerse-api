from django.urls import path
from .api import OrderView, CreateOrder, UpdateOrder

urlpatterns = [
    path('order/<pk>/', OrderView.as_view(), name='view_order'),
    path('order/create/', CreateOrder.as_view(), name='create_order'),
    path('order/update/<pk>', UpdateOrder.as_view(), name='update_order')
]
