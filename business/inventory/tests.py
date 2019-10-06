from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from .models import Supplier, Product


class UserTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = self.setup_user()
        self.token = Token.objects.create(user=self.user)
        self.token.save()

    @staticmethod
    def setup_user():
        user = get_user_model()
        return user.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )


test_supplier_params = {
    "identifier": "test-supplier",
    "name": "Test Supplier",
    "phone_number": "+254797797797",
    "email": "test@email.com"
}
test_product_params = {
    "name": "Test Product",
    "weight": 4.34,
    "supplier": 1,
    "size": 1
}


def create_test_supplier():
    supplier = Supplier(**test_supplier_params)
    supplier.save()


def create_test_product():
    product = Product(**{
        "name": "Test Product",
        "weight": 4.34,
        "size": 1,
    })
    product.save()
    product.supplier.set([1])


# supplier tests
class TestCreateSupplier(UserTestCase):

    def setUp(self):
        super().setUp()

    def test_create_supplier(self):
        url = reverse("inventory:add_supplier")
        response = self.client.post(url, test_supplier_params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))


class TestRetrieveSupplier(UserTestCase):
    def setUp(self):
        super().setUp()
        create_test_supplier()
        # create_test_product()

    def test_retrieve_supplier(self):
        """
        Test the retrieval of  product data  an inventory object
        :return: None
        """
        self.client.login(username="test", password="test")
        url = reverse('inventory:supplier_view', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Retrieve Supplier is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_update_supplier(self):
        self.client.login(username="test", password="test")
        url = reverse('inventory:supplier_view', kwargs={'pk': 1})
        response = self.client.put(url, data={
            "identifier": "test-supplier-update",
            "name": "Test Supplier Update",
            "phone_number": "+254797797797",
            "email": "test@email.com"
        })
        self.assertEqual(response.status_code, 200,
                         'Retrieve Supplier is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_delete_supplier(self):
        self.client.login(username="test", password="test")
        url = reverse('inventory:supplier_view', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204,
                         'Delete Supplier is not Successful.\n'
                         'Expected  Response Code 204, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_list_suppliers(self):
        self.client.login(username="test", password="test")
        url = reverse('inventory:list_suppliers')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Listing of Suppliers is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))


# product tests
class TestCreateProduct(UserTestCase):

    def setUp(self):
        super().setUp()
        create_test_supplier()

    def test_create_product(self):
        """
        Test whether a user can create an inventory object
        :return: None
        """
        self.client.login(username="test", password="test")
        url = reverse('inventory:add_product')
        params = {
            "name": "Test Product",
            "weight": 4.34,
            "supplier": [1],
            "size": 1
        }
        response = self.client.post(url, params)
        self.assertEqual(response.status_code, 201,
                         'Expected Response Code 201, received {0} instead.'
                         .format(response.status_code))


class TestRetrieveProduct(UserTestCase):
    def setUp(self):
        super().setUp()
        create_test_supplier()
        create_test_product()

    def test_retrieve_product(self):
        """
        Test the retrieval of  product data  an inventory object
        :return: None
        """

        self.client.login(username="test", password="test")
        url = reverse('inventory:product_view', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Retrieve Product is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_update_product(self):
        self.client.login(username="test", password="test")
        url = reverse('inventory:product_view', kwargs={'pk': 1})
        response = self.client.put(url, data={
            "name": "Test Product Update",
            "weight": 4.34,
            "supplier": [1],
            "size": 1
        })
        self.assertEqual(response.status_code, 200,
                         'Retrieve Product is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, bytes.decode(response.content)))

    def test_delete_product(self):
        self.client.login(username="test", password="test")
        url = reverse('inventory:product_view', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204,
                         'Delete Product is not Successful.\n'
                         'Expected  Response Code 204, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))

    def test_list_products(self):
        self.client.login(username="test", password="test")
        url = reverse('inventory:list_products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Listing of Products is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))
