from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

from .models import Order
from .serializers import OrderSerializer


class CreateOrder(CreateAPIView):
    serializer_class = OrderSerializer


class OrderView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            orderinfo__delivery_info__user=self.request.user
        )
