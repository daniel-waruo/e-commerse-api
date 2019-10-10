from rest_framework.reverse import reverse

from client.cart.utils import add_product_to_cart
from client.delivery.tests import create_delivery_info_object
from utils.tests import TestAuthenticatedUser, create_test_cms_product


class TestCheckout(TestAuthenticatedUser):
    def setUp(self):
        super().setUp()
        create_delivery_info_object(self.user.id)

        """ 
        TODO: 
            create test cart
            create test delivery information
            create test receipt id
        """

    def test_checkout_empty_cart(self):
        url = reverse("checkout:checkout")
        response = self.client.post(url, {
            "cart_id": 1,
            "delivery_info_id": 1,
            "receipt_id": ''
        })
        self.assertEqual(response.status_code, 400,
                         'Checkout  is Successful.Expected Response Code 400, received {0} instead.'
                         'It returned \n{1}.GO and look at your logic'
                         .format(response.status_code, response.content))

    def test_checkout_with_cart(self):
        create_test_cms_product()
        add_product_to_cart(product_pk=1, user_id=self.user.id)
        url = reverse("checkout:checkout")
        response = self.client.post(url, {
            "cart_id": 1,
            "delivery_info_id": 1,
            "receipt_id": ''
        })
        self.assertEqual(response.status_code, 201,
                         'Checkout  is not Successful.Expected Response Code 201, received {0} instead.'
                         'It returned \n{1}.'
                         .format(response.status_code, response.content))
