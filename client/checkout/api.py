from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from business.orders.models import ProductOrder
from business.orders.serializers import OrderSerializer
from client.cart.models import Cart, CartProduct
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

        # cart_id = request.POST.get("cart_id")
        delivery_info_id = request.POST.get("delivery_info_id")
        receipt_id = request.POST.get("receipt_id")

        data = {
            "user": request.user.id,
            "delivery_info": delivery_info_id
        }
        # TODO:check whether the user is eligible for pay on delivery

        serializer = OrderSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        cart = get_cart_object(user_id=self.request.user.id)
        # TODO: check whether cart products is empty and return a 404 response
        cartproducts = CartProduct.objects.filter(cart_id=cart.id)
        if not cartproducts:
            raise ValidationError("The Cart is empty therefore one cannot checkout")

        def cartproduct_to_productorder(cart_product):
            product_order = ProductOrder(
                order=order,
                product=cart_product.product,
                number=cart_product.number,
            )
            product_order.save()

        map(cartproduct_to_productorder, cartproducts)

        Cart.objects.get(id=cart.id).delete()

        return Response(status=status.HTTP_201_CREATED)
