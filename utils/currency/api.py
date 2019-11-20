from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .utils import get_currency_from_ip


# Create your views here.
class SetCurrencyAPI(GenericAPIView):
    """"
    This is the Update Currency View of the API
    """

    def post(self, request, *args, **kwargs):
        if request.POST.get('currency', None):
            currency = request.POST.get('currency')
        else:
            currency = get_currency_from_ip(request)
        return Response({
            'currency': currency
        }).set_cookie('currency', currency)
