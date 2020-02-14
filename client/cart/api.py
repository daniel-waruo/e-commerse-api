from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
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
    get_cart_object
)


class CartApiView(APIView):
    permission_classes = [AllowAny]
    # This is the status that the view return in the response when successfull
    success_status = status.HTTP_200_OK
    required_post_fields = ['product_pk']

    def get_required_fields(self):
        # gets the required post fields for this view
        fields = self.required_post_fields
        # checks if the fields are all present in the POST data and returns an error
        # if it is not there
        for field in fields:
            if not self.request.POST.get(field):
                raise ValidationError("The field " + field + " is required")

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.user = request.user
        self.checkout_session = request.checkout_session
        # check whether the user is authenticates and assign the appropriate kwargs for use in
        # getting the cart objects
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
        # check if the required fields are there
        self.get_required_fields()
        # do the specific cart product action and return the cart product object
        self.cart_product = self.product_action()
        # get data to be returned
        data = self.get_data()
        # return the response
        return Response(data, status=self.success_status)

    def get_cart_details(self):
        # get the cart details
        if self.request.user.is_authenticated:
            return CartDetails(user_id=self.user.id)
        else:
            return CartDetails(session=self.checkout_session.session_key)

    def get_data(self):
        """
        This method returns the data useful to the cart views
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
        product_number = self.request.POST.get("product_number", 1)
        return add_product_to_cart(product_pk=pk, **self.user_session_kwargs, product_number=product_number)


class RemoveProduct(CartApiView):
    success_status = status.HTTP_204_NO_CONTENT

    def product_action(self):
        pk = self.request.POST.get("product_pk", None)
        return remove_product_from_cart(pk, **self.user_session_kwargs)


class UpdateProductNumber(CartApiView):
    required_post_fields = ['product_pk', 'product_number']

    def product_action(self):
        self.pk = self.request.POST.get('product_pk', None)
        product_number = self.request.POST.get('product_number', None)
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


class CartView(RetrieveAPIView):
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
