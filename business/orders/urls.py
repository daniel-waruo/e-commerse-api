from django.urls import path

from .api import OrderView

app_name = 'orders'

urlpatterns = [
    path('order/<pk>', OrderView.as_view(), name='view_order')
]
