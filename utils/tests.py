from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model
from djmoney.money import Money
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from business.cms.models import Category, Product as CmsProduct
from business.inventory.models import Supplier, Product as InventoryProduct


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


class TestAuthenticatedUser(UserTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)


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


test_category_params = {
    "name": "Test Category",
    "slug": "test-category",
    "parent": ''
}
# TODO: find  out how to represent multipart fields in django rest framework
test_cms_product_params = {
    "product": 1,
    "name": "Test Cms Product",
    "images": ["", "", ""],
    "category": 1,
    "price": (2000.87, 'USD'),
    "discount_price": 1800.87,
    "slug": "cms-product",
    "description": "This is the Product Used to test our Cms Product"
}


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
