from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils import (
    add_product_to_cart,
    remove_product_from_cart,
    update_product_number,
    update_cart)


class CartApiView(APIView):
    permission_classes = (AllowAny,)
    # This is the status that the view return in the response when successfull
    success_status = status.HTTP_200_OK
    success_message = 'Operation Successful'
    required_post_fields = ['product_pk']

    def get_user_session_kwargs(self):
        # check whether the user is authenticates and assign the appropriate kwargs for use in
        # getting the cart objects
        user = self.request.user
        session_key = self.request.checkout_session.session_key
        if user.is_authenticated:
            return {'user_id': user.id}
        return {'session_key': session_key}

    def get_required_fields(self):
        # gets the required post fields for this view
        fields = self.required_post_fields
        # checks if the fields are all present in the POST data and returns an error
        # if it is not there
        for field in fields:
            # raise Exception(self.request.data.get(field))
            if not self.request.data.get(field):
                raise ValidationError("The field " + field + " is required")

    def product_action(self):
        """
        This method performs a product related action on a product and returns the cart product
        :return:CartProduct(object)
        """
        raise NotImplementedError("This must be implemented in the View")

    def get_success_message(self):
        return self.success_message

    def post(self, request, *args, **kwargs):
        self.request = request
        # check if the required fields are there
        self.get_required_fields()
        # do the an action to the cart
        self.product_action()

        # get success message by this time if there were any errors they will be handled
        message = self.get_success_message()
        # return the response
        return Response({'data': message}, status=self.success_status)


class AddProduct(CartApiView):
    required_post_fields = ['product_pk', 'product_number']
    success_status = status.HTTP_201_CREATED

    def product_action(self):
        pk = self.request.data.get("product_pk", None)
        product_number = self.request.data.get("product_number", 1)
        add_product_to_cart(product_pk=pk, **self.get_user_session_kwargs(), product_number=product_number)


class RemoveProduct(CartApiView):
    required_post_fields = ['product_pk']

    def product_action(self):
        pk = self.request.data.get("product_pk", None)
        remove_product_from_cart(pk, **self.get_user_session_kwargs())


class UpdateProductNumber(CartApiView):
    required_post_fields = ['product_pk', 'product_number']

    def product_action(self):
        pk = self.request.data.get('product_pk', None)
        product_number = self.request.data.get('product_number', None)
        update_product_number(product_pk=pk, product_number=product_number,
                              **self.get_user_session_kwargs())


class UpdateCart(CartApiView):
    required_post_fields = ['products']
    success_message = "Cart Update Successful"

    def product_action(self):
        products = self.request.data.get('products')
        update_cart(products, **self.get_user_session_kwargs())
