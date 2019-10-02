from django.http import JsonResponse
from django.views.generic import View
from ordersapp.models import ProductOrder


# Create your views here.


class ChangeProductOrderState(View):
    def get_order_object(self, product_order_id):
        return ProductOrder.objects.get(order_id=product_order_id)

    def post(self, request, product_order_id):
        state = request.POST.get('state', 'init')
        product_order = self.get_order_object(product_order_id)
        product_order.state = state
        product_order.save()
        return JsonResponse(
            data={
                "success": True,
                "content": {
                    "state": state
                }
            }
        )
