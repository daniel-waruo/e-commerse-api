from rest_framework import status
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response

from business.authorization.permissions import IsDepartmentMember
from .models import Order
from .serializers import OrderSerializer


class OrderView(RetrieveAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()


class ChangeOrderStatus(GenericAPIView):
    permission_classes = [IsDepartmentMember, DjangoModelPermissions]

    # serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(
            state="pending"
        )

    def post(self, request, *args, **kwargs):
        return Response(status.HTTP_200_OK)
