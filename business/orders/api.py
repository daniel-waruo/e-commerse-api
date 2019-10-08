from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Order
from .serializers import OrderSerializer


class OrderView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()
