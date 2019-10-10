from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import DjangoModelPermissions

from .models import Order
from .serializers import OrderSerializer


class OrderView(RetrieveUpdateDestroyAPIView):
    permission_classes = [DjangoModelPermissions]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()
