from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from business.orders.models import ProductOrder
from business.orders.serializers import OrderSerializer
from client.cart.models import CartProduct
from client.cart.utils import get_cart_object


class CheckoutApi(APIView):
    """
    Checkout Api View
    This is the view that transitions from a cart to an order

    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # TODO:check whether user has a cart object if not redirect to products
        """
        takes data in this schema
            "delivery_info_id"
        :param request:
        :return:
        """
        cart = get_cart_object(user_id=self.request.user.id)
        cartproducts = CartProduct.objects.filter(cart_id=cart.id)
        if not cartproducts:
            raise ValidationError("The Cart is empty therefore one cannot checkout")

        delivery_info_id = request.POST.get("delivery_info_id")
        receipt_id = request.POST.get("receipt_id")
        # TODO: create a machine learning model to learn if user requires given receipt id
        if not receipt_id:
            # check if user can checkout without valid receipt
            if False:
                raise ValidationError("The User Is not allowed to Pay on Delivery")
        serializer = OrderSerializer(
            data={
                "user": request.user.id,
                "delivery_info": delivery_info_id
            }
        )
        serializer.is_valid(raise_exception=True)
        # get the order object
        order = serializer.save()
        list(map(
            lambda cart_product: print(ProductOrder.objects.create(
                order=order,
                product=cart_product.product,
                number=cart_product.number,
            )),
            cartproducts
        ))
        # delete the cart after transferring to the order
        cart.delete()
        return Response(status=status.HTTP_201_CREATED)
