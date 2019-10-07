from django.http import HttpResponseBadRequest
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.currency.utils import translate_money
from .serializers import CartSerializer
from .utils import (
    add_product_to_cart,
    remove_product_from_cart,
    add_product_number,
    subtract_product_number,
    update_product_number,
    CartDetails,
    get_cart_object)


class CartApiView(APIView):
    # This is the status that the view return in the response when successfull
    success_status = status.HTTP_200_OK
    required_post_fields = ['product_pk']

    def get_required_fields(self):
        fields = self.required_post_fields
        for field in fields:
            if field not in self.request.POST:
                return HttpResponseBadRequest

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = request.user
        self.checkout_session = request.checkout_session
        if request.user.is_authenticated:
            self.user_session_kwargs = {
                'user_id': request.user.id
            }
        else:
            self.user_session_kwargs = {
                'session_key': request.checkout_session.session_key
            }
        return super().dispatch(request, args, **kwargs)

    def product_action(self):
        """
        This method performs a product related action on a product and returns the cart product
        :return:CartProduct(object)
        """
        raise NotImplementedError("This must be implemented in the View")

    def post(self, request, *args, **kwargs):
        self.get_required_fields()
        self.cart_product = self.product_action()
        data = self.get_data()
        return Response(data, status=self.success_status)

    def get_cart_details(self):
        if self.request.user.is_authenticated():
            return CartDetails(user_id=self.user.id)
        else:
            return CartDetails(session=self.checkout_session.session_key)

    def get_data(self):
        """
        This method returns the data usefull to cart views
        :return:data
        """
        cart_details = self.get_cart_details()
        data = {
            'cart_detail': {
                'cart_total_number': cart_details.total_number,
                'cart_total_value': str(
                    translate_money(
                        self.request,
                        cart_details.total_value
                    )
                )
            }
        }
        return data


class AddProduct(CartApiView):
    success_status = status.HTTP_201_CREATED

    def product_action(self):
        pk = self.request.POST.get("product_pk", None)
        return add_product_to_cart(product_pk=pk, **self.user_session_kwargs)


class RemoveProduct(CartApiView):
    success_status = status.HTTP_204_NO_CONTENT

    def product_action(self):
        pk = self.request.POST.get("product_pk", None)
        return remove_product_from_cart(pk, **self.user_session_kwargs)


class AddProductNumber(CartApiView):
    def product_action(self):
        self.pk = self.request.POST.get("product_pk", None)
        return add_product_number(product_pk=self.pk, **self.user_session_kwargs)

    def get_data(self):
        data = super().get_data()
        data.update(
            {
                "product_pk": self.pk,
                "product_total": str(
                    translate_money(
                        self.request,
                        self.cart_product.product.price * self.cart_product.number
                    )),
            }
        )
        return data


class SubtractProductNumber(CartApiView):
    def product_action(self):
        self.pk = self.request.POST.get("product_pk", None)
        return subtract_product_number(product_pk=self.pk, **self.user_session_kwargs)

    def get_data(self):
        data = super().get_data()
        data.update(
            {
                "product_pk": self.pk,
                "product_total": str(
                    translate_money(
                        self.request,
                        self.cart_product.product.price * self.cart_product.number
                    )),
            }
        )
        return data


class UpdateProductNumber(CartApiView):
    required_post_fields = ['product_pk', 'product_number']

    def product_action(self):
        self.pk = self.request.POST.get('product_pk', None)
        product_number = self.request.POST('product_number', None)
        return update_product_number(product_pk=self.pk, product_number=product_number, **self.user_session_kwargs)

    def get_data(self):
        data = super().get_data()
        data.update(
            {
                "product_pk": self.pk,
                "product_total": str(
                    translate_money(
                        self.request,
                        self.cart_product.product.price * self.cart_product.number
                    )),
            }
        )
        return data


class CartListView(RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return get_cart_object(
                user_id=self.request.user.id
            )
        else:
            return get_cart_object(
                session_key=self.request.checkout_session.session_key
            )
