from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart


class CartApiView(APIView):
    permission_classes = (AllowAny,)
    # This is the status that the view return in the response when successfull
    success_status = status.HTTP_200_OK
    success_message = 'Operation Successful'
    required_post_fields = ['product_pk']

    def __init__(self, **kwargs):
        self.cart = None
        super().__init__(**kwargs)

    def dispatch(self, request, *args, **kwargs):
        # set self cart
        self.cart = Cart.objects.get_from_request(request)
        return super().dispatch(request, *args, **kwargs)

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
        # get product pj from request
        pk = self.request.data.get("product_pk", None)
        # get product number from request
        product_number = self.request.data.get("product_number", 1)
        # add product to cart
        self.cart.add_product(product_pk=pk, product_number=product_number)


class RemoveProduct(CartApiView):
    required_post_fields = ['product_pk']

    def product_action(self):
        # get product pk from request data
        pk = self.request.data.get("product_pk", None)
        # remove product from cart
        self.cart.remove_product(product_pk=pk)


class UpdateProductNumber(CartApiView):
    required_post_fields = ['product_pk', 'product_number']

    def product_action(self):
        # get product pk from request
        pk = self.request.data.get('product_pk', None)
        # get product number from request
        product_number = self.request.data.get('product_number', None)
        # update product number
        self.cart.update_product_number(product_pk=pk, product_number=product_number)


class UpdateCart(CartApiView):
    required_post_fields = ['products']
    success_message = "Cart Update Successful"

    def product_action(self):
        # get products from request
        products = self.request.data.get('products')
        # update cart
        self.cart.update_cart(products=products)
