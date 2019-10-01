from braces.views import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from checkout.utils import get_grand_total, get_checkout_id
from front_end.template_names import template_
from transactionsapp.forms import MpesaTransactionForm


# Create your views here.


class TransactionFormView(View):

    def get(self, request, payment_method):
        pass


class MakePhoneTransactionView(LoginRequiredMixin, View):

    def get_success_url(self):
        pass

    def post(self, request):
        money = get_grand_total(
            get_checkout_id(request.user.id)
        )
        print(money)
        form = MpesaTransactionForm(data=request.POST)
        if form.is_valid():
            response = form.pay(money)
            print(response)
            request.session["pending_transaction"] = {
                "id": response.get("transactionId",''),
                "providerChannel": response.get("providerChannel",'')
            }
            data = {
                "success": True,
                "content": response.get("description",'')
            }
        else:
            data = {
                "errors": form.errors
            }
        return JsonResponse(data=data)


"""
    order = Order()
    order.user = request.user
    order.mobile_transaction_data = {
        "phonenumber": phonenumber,
        "amount": money.amount,
        "email": request.user.email,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name
    }
    order.send_email_message_confirmation()
    return redirect(self.success_url)
"""


@method_decorator(csrf_exempt, name='dispatch')
class TransactionCallback(View):
    def get(self, request):
        return JsonResponse(
            data={
                'success': True
            }
        )

    def post(self, request):
        return JsonResponse(
            data={
                'success': True
            }
        )


transaction_callback = TransactionCallback.as_view()


def order_confirm(request):
    return render(request, template_["order_confirm"])
