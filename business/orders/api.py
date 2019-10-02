from rest_framework.generics import RetrieveAPIView, CreateAPIView
from .serializers import OrderSerializer


class OrderView(RetrieveAPIView):
    serializer_class = OrderSerializer


class CreateOrder(CreateAPIView):
    serializer_class = OrderSerializer


class UpdateOrder(CreateOrder):
    serializer_class = OrderSerializer
