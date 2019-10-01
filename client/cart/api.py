from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.currency.utils import translate_money
from .utils import (
    add_product_to_cart,
    remove_product_from_cart,
    add_product_number,
    subtract_product_number,
    CartDetails
)


class AddProduct(APIView):

    def post(self, request):
        pk = request.POST.get("product_pk", None)
        if not pk:
            raise Http404("No pk on post data")
        if request.user.is_authenticated:
            user_id = request.user.id
            add_product_to_cart(product_pk=pk, user_id=user_id)
            cart_details = CartDetails(user_id=user_id)
        else:
            session_key = request.checkout_session.session_key
            add_product_to_cart(product_pk=pk, session_key=session_key)
            cart_details = CartDetails(session=session_key)
        data = {
            'cart_detail': {
                'cart_total_number': cart_details.total_number,
                'cart_total_value': str(
                    translate_money(
                        request,
                        cart_details.total_value
                    )
                )
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)


class RemoveProduct(APIView):

    def post(self, request):
        pk = request.POST.get("product_pk", None)
        if not pk:
            raise Http404("No pk on post data")
        if request.user.is_authenticated:
            user_id = request.user.id
            remove_product_from_cart(pk, user_id=user_id)
            cart_details = CartDetails(user_id=user_id)
        else:
            session_key = request.checkout_session.session_key
            remove_product_from_cart(pk, session_key=session_key)
            cart_details = CartDetails(session=session_key)
        data = {
            'cart_detail': {
                'cart_total_number': cart_details.total_number,
                'cart_total_value': str(
                    translate_money(
                        request,
                        cart_details.total_value
                    )
                )
            }
        }
        return Response(data, status=status.HTTP_200_OK)


class AddProductNumber(APIView):
    def post(self, request):
        pk = request.POST.get("product_pk", None)
        if not pk:
            raise Http404()
        if request.user.is_authenticated:
            cart_product = add_product_number(product_pk=pk, user_id=request.user.id)
            cart_details = CartDetails(user_id=request.user.id)
        else:
            session_key = request.checkout_session.session_key
            # the function returns the product checkout
            cart_product = add_product_number(product_pk=pk, session_key=session_key)
            cart_details = CartDetails(session=session_key)
        data = {
            'cart_detail': {
                'cart_total_number': cart_details.total_number,
                'cart_total_value': str(
                    translate_money(
                        request,
                        cart_details.total_value
                    )
                )
            },
            "product_pk": pk,
            "product_total": str(
                translate_money(
                    request,
                    cart_product.product.price * cart_product.number
                )),
        }
        return Response(data, status=status.HTTP_200_OK)


class SubtractProductNumber(APIView):
    def post(self, request):
        pk = request.POST.get("product_pk", None)
        if not pk:
            raise Http404()
        if request.user.is_authenticated:
            cart_product = subtract_product_number(product_pk=pk, user_id=request.user.id)
            cart_details = CartDetails(user_id=request.user.id)
        else:
            session_key = request.checkout_session.session_key
            # the function returns the product checkout
            cart_product = subtract_product_number(product_pk=pk, session_key=session_key)
            cart_details = CartDetails(session=session_key)
        data = {
            'cart_detail': {
                'cart_total_number': cart_details.total_number,
                'cart_total_value': str(
                    translate_money(
                        request,
                        cart_details.total_value
                    )
                )
            },
            "product_pk": pk,
            "product_total": str(
                translate_money(
                    request,
                    cart_product.product.price * cart_product.number
                )),
        }
        return Response(data, status=status.HTTP_200_OK)
