from importlib import import_module

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from djmoney.money import Money
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from accounts.models import StaffUser
from business.authorization.utils import get_all_department_ids
from business.cms.models import Category, Product as CmsProduct
from business.inventory.models import Supplier, Product as InventoryProduct


class UserTestCase(APITestCase):
    # register domain as we are using django.contrib.sites
    @staticmethod
    def _create_site_config():
        Site.objects.create(
            name='Test Server',
            domain='testserver'
        )

    def setUp(self):
        self._create_site_config()
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


class TestAuthenticatedUser(UserTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)


class TestSuperUserPermissions(TestAuthenticatedUser):
    @staticmethod
    def setup_user():
        user = get_user_model()
        return user.objects.create_superuser(
            username='test',
            email='testuser@test.com',
            password='test'
        )


class TestStaffSuperUser(TestSuperUserPermissions):
    """
    Test the Creation Of a Staff User
    """

    def create_departments(self):
        # import all app configs
        app_configs = apps.get_app_configs()

        # function takes in an appconfig and runs the .ready method
        list(map(lambda app_config: app_config.ready(), app_configs))

    def create_user(self):
        user = get_user_model()
        return user.objects.create_user(
            **{
                'username': "test-username-2",
                'email': "test-2@gmail.com",
                'password': 'test-password',
            }
        )

    def create_staff_user(self, user_id):
        staff = StaffUser(
            user_id=user_id,
            staff_type=3
        )
        staff.save()
        staff.departments.set(get_all_department_ids())
        return staff

    def setUp(self):
        super().setUp()
        self.create_departments()
        self.create_staff_user(self.user.id)


def unauthorised_message(response):
    return """
    Authorization failed.Expected Response Code 401, received {0} instead.
    Response data is:
           \t{1}
           
    """.format(response.status_code, response.content)


def unsuccessful_message(response, action, expected_code):
    return """ 
           '{0} not successful.
           Expected Response Code {1}, received {2} instead.
           Response data is:
           \t{3}
           """.format(action, expected_code, response.status_code, response.data)


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


def create_test_inventory_product():
    create_test_supplier()
    product = InventoryProduct(**{
        "name": "Test Product",
        "weight": 4.34,
        "size": 1,
    })
    product.save()
    product.supplier.set([1])


class TestSupplierMixin:

    def create_supplier(self):
        """
        Creates a supplier
        :return:response
        """
        url = reverse("inventory:add_supplier")
        return self.client.post(url, test_supplier_params)

    def retrieve_supplier(self):
        """
        Retrieves a supplier
        :return: response
        """
        url = reverse('inventory:supplier_view', kwargs={'pk': 1})
        return self.client.get(url)

    def update_supplier(self):
        """
        Updates a supplier
        :return: response
        """
        url = reverse('inventory:supplier_view', kwargs={'pk': 1})
        return self.client.put(url, data={
            "identifier": "test-supplier-update",
            "name": "Test Supplier Update",
            "phone_number": "+254797797797",
            "email": "test@email.com"
        })

    def delete_supplier(self):
        url = reverse('inventory:supplier_view', kwargs={'pk': 1})
        return self.client.delete(url)

    def list_supplier(self):
        url = reverse('inventory:list_suppliers')
        return self.client.get(url)


class TestInventoryProductMixin:
    def create_product(self):
        """
        Test whether a user can create an inventory object
        :return: None
        """
        url = reverse('inventory:add_product')
        params = {
            "name": "Test Product",
            "weight": 4.34,
            "supplier": [1],
            "size": 1
        }
        return self.client.post(url, params)

    def update_product(self):
        url = reverse('inventory:product_view', kwargs={'pk': 1})
        return self.client.put(url, data={
            "name": "Test Product Update",
            "weight": 4.34,
            "supplier": [1],
            "size": 1
        })

    def retrieve_product(self):
        """
        Test the retrieval of  product data  an inventory object
        :return: None
        """
        url = reverse('inventory:product_view', kwargs={'pk': 1})
        return self.client.get(url)

    def list_product(self):
        url = reverse('inventory:list_products')
        return self.client.get(url)

    def delete_product(self):
        url = reverse('inventory:product_view', kwargs={'pk': 1})
        return self.client.delete(url)


class CheckoutSessionTestMixin:
    def checkout_session(self):
        """Return the current session variables."""
        engine = import_module(settings.ANONYMOUS_SESSION_ENGINE)
        cookie = self.client.cookies.get(settings.ANONYMOUS_SESSION_NAME)
        if cookie:
            return engine.CheckoutSessionStore(session_key=cookie.value)

        session = engine.CheckoutSessionStore()
        session.save()
        self.client.cookies[settings.ANONYMOUS_SESSION_NAME] = session.session_key
        return session


def create_test_category():
    category = Category(
        **{
            "name": "Test Category",
            "slug": "test-category",
        }
    )
    category.save()


def create_test_cms_product():
    create_test_inventory_product()
    create_test_category()
    product = CmsProduct(**{
        "product_id": 1,
        "name": "Test Cms Product",
        "images": "",
        "category_id": 1,
        "price": Money(2000.87, "USD"),
        "discount_price": Money(1800.87, "USD"),
        "slug": "cms-product",
        "description": "This is the Product Used to test our Cms Product"
    })
    product.save()


class TestCmsProductMixin:
    """
    every method returns a response
    """

    def create_product(self):
        url = reverse("cms:add_product")
        return self.client.post(url, data={
            "product": 1,
            "name": "Test Cms Product",
            # "images": ["https://ucarecdn.com/0799e306-6da7-4c94-bc54-29cf96957f25/-/resize/50x50/"],
            "category": 1,
            "price": 2000.87,
            "price_currency": "USD",
            "discount_price": 1800.87,
            "discount_price_currency": "USD",
            "slug": "cms-product",
            "description": "This is the Product Used to test our Cms Product"
        })

    def retrieve_product(self):
        url = reverse('cms:product_view', kwargs={'pk': 1})
        return self.client.get(url)

    def update_product(self):
        url = reverse('cms:product_view', kwargs={'pk': 1})
        return self.client.put(url, data={
            "product": 1,
            "name": "Test Cms Product Update",
            "images": ["", "", ""],
            "category": 1,
            "price": 2000.87,
            "discount_price": 1800.87,
            "slug": "cms-product-update",
            "description": "This is the Product Used to test our Cms Product"
        })

    def delete_product(self):
        url = reverse('cms:product_view', kwargs={'pk': 1})
        return self.client.delete(url)

    def list_product(self):
        url = reverse('cms:list_products')
        return self.client.get(url)


class TestCategoryMixin:
    """
    every method returns a response
    """

    def create_category(self):
        url = reverse("cms:add_category")
        return self.client.post(url, data={
            "name": "Test Category",
            "slug": "test-category",
            "parent": ''
        })

    def retrieve_category(self):
        url = reverse('cms:category_view', kwargs={'pk': 1})
        return self.client.get(url)

    def update_category(self):
        url = reverse('cms:category_view', kwargs={'pk': 1})
        return self.client.put(url, data={
            "name": "Test Category Update",
            "slug": "test-category-update",
            "parent": ''
        })

    def delete_category(self):
        url = reverse('cms:category_view', kwargs={'pk': 1})
        return self.client.delete(url)

    def list_category(self):
        url = reverse('cms:list_categories')
        return self.client.get(url)
