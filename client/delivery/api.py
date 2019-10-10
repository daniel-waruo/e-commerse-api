from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from client.delivery.models import DeliveryInfo
from .serializers import DeliveryInfoSerializer


class CreateDeliveryInfo(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryInfoSerializer

    def get_queryset(self):
        return DeliveryInfo.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        data = request.data.dict()
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeliveryInfoApi(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryInfoSerializer

    def get_queryset(self):
        return DeliveryInfo.objects.filter(
            user_id=self.request.user.id
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.dict()
        data["user"] = request.user.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class ListDeliveryInfo(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeliveryInfoSerializer

    def get_queryset(self):
        return DeliveryInfo.objects.filter(
            user_id=self.request.user.id
        )

