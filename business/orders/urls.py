from django.urls import path

from .api import OrderView, ChangeOrderStatus

app_name = 'orders'

urlpatterns = [
    path('order/<str:pk>', OrderView.as_view(), name='view_order'),
    path('order/status/<str:pk>', ChangeOrderStatus.as_view(), name='change_order_status')
]
