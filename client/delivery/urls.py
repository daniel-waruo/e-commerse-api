from django.urls import path

from .api import CreateDeliveryInfo, DeliveryInfoApi, ListDeliveryInfo

app_name = 'delivery'

urlpatterns = [
    path('delivery-information/add', CreateDeliveryInfo.as_view(), name='add_delivery_info'),
    path('delivery-information/<int:pk>', DeliveryInfoApi.as_view(), name='delivery_info'),
    path('delivery-information/list', ListDeliveryInfo.as_view(), name='list_delivery_info')
]
