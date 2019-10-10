from rest_framework.reverse import reverse

from client.cart.utils import add_product_to_cart
from utils.tests import CheckoutSessionTestMixin
from utils.tests import UserTestCase, create_test_cms_product


def create_cart_product(product_pk, user_id=None, session_key=None):
    create_test_cms_product()
    add_product_to_cart(
        product_pk=product_pk,
        user_id=user_id,
        session_key=session_key
    )


class TestCartAuthenticatedUser(UserTestCase):
    """
    Tests the Cart operations of an authenticated user
    """

    def setUp(self):
        super().setUp()
        # force authenticate the user
        self.client.force_login(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)

    def test_add_product(self):
        """
        Test the addition of a product to the cart
        :return: None
        """
        create_test_cms_product()
        url = reverse('cart:cart_add_product')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 201,
                         'Add Product to Cart is not Successful.\n'
                         'Expected  Response Code 201, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_remove_product(self):
        """
        Test the removal of a product from the cart
        :return: None
        """
        create_cart_product(1, user_id=self.user.id)
        url = reverse('cart:cart_remove_product')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 204,
                         'Remove product from cart is not Successful.\n'
                         'Expected  Response Code 204, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_add_product_number(self):
        """
        Test the addition of number of a product
        :return: None
        """
        create_cart_product(1, user_id=self.user.id)
        url = reverse('cart:cart_add_product_number')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 200,
                         'Add Number of Products is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_subtract_product_number(self):
        """
        Test the subtraction of the numbers of a product
        :return: None
        """
        create_cart_product(1, user_id=self.user.id)
        url = reverse('cart:cart_subtract_product_number')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 200,
                         'Subtract number of products  in Cart is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_update_product_number(self):
        """
        Test the update of the number of a product
        :return: None
        """
        create_cart_product(1, user_id=self.user.id)
        url = reverse('cart:cart_update_product_number')
        response = self.client.post(url, data={"product_pk": 1, "product_number": 34})
        self.assertEqual(response.status_code, 200,
                         'Update number of products  in Cart is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))


class TestCartAnonymousUser(UserTestCase, CheckoutSessionTestMixin):
    """
    Tests the Cart operations of an authenticated user
    """

    def setUp(self):
        super().setUp()
        self.session_key = self.checkout_session().session_key
        # get the session key

    def test_add_product(self):
        """
        Test the addition of a product to the cart
        :return: None
        """
        create_test_cms_product()
        url = reverse('cart:cart_add_product')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 201,
                         'Add Product to Cart is not Successful.\n'
                         'Expected  Response Code 201, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_remove_product(self):
        """
        Test the removal of a product from the cart
        :return: None
        """
        # raise Exception(self.checkout_session().session_key)
        create_cart_product(1, session_key=self.session_key)
        url = reverse('cart:cart_remove_product')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 204,
                         'Remove product from cart is not Successful.\n'
                         'Expected  Response Code 204, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_add_product_number(self):
        """
        Test the addition of number of a product
        :return: None
        """
        create_cart_product(1, session_key=self.session_key)
        url = reverse('cart:cart_add_product_number')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 200,
                         'Add Number of Products is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_subtract_product_number(self):
        """
        Test the subtraction of the numbers of a product
        :return: None
        """
        create_cart_product(1, session_key=self.session_key)
        url = reverse('cart:cart_subtract_product_number')
        response = self.client.post(url, data={"product_pk": 1})
        self.assertEqual(response.status_code, 200,
                         'Subtract number of products  in Cart is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_update_product_number(self):
        """
        Test the update of the number of a product
        :return: None
        """
        create_cart_product(1, session_key=self.session_key)
        url = reverse('cart:cart_update_product_number')
        response = self.client.post(url, data={"product_pk": 1, "product_number": 34})
        self.assertEqual(response.status_code, 200,
                         'Update number of products  in Cart is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))
