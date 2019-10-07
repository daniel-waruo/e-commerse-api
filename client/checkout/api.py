from rest_framework.views import APIView


class CheckoutApi(APIView):
    """
    Checkout Api View
    This is the view that transitions from a cart to an order

    """

    def post(self, request):
        """
        takes data in this schema
            "order": payment_status,
            ""
            "delivery_info_id"
            "cart_id":
        :param request:
        :return:
        """
        pass
