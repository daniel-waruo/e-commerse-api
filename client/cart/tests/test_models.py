from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase
from djmoney.money import Money
from knox.models import AuthToken
from rest_framework.test import APIClient, APIRequestFactory

from business.products.models import Product, Category
from client.cart.errors import NoProductToDelete
from client.cart.models import Cart, CartProduct
from utils.session.middleware import AnonymousSessionMiddleware

User = get_user_model()


class CartManagerTestCase(TestCase):
    """ Test Methods added by the Cart Manager """

    def setUp(self):
        """ Create and Authenticate a User """
        self.user = User.objects.create_user(
            username='john',
            email='johndoe@gmail.com',
            password='password'
        )
        self.client = APIClient()
        token, token_string = AuthToken.objects.create(user=self.user)
        self.token = token
        self.request = APIRequestFactory().get('/')
        self.request.user = AnonymousUser()

    def _authenticate_user(self):
        """ Mock Authentication by adding the user object to the request instance """
        self.request.user = self.user

    def _run_middleware(self):
        """ Set Required Middleware to sustain an anonymous session """
        middleware = SessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()
        middleware = AnonymousSessionMiddleware()
        middleware.process_request(self.request)
        self.request.session.save()

    def test_cart_creation_from_authenticated_user(self):
        """ Test whether cart is created from authenticated User """
        self._authenticate_user()
        cart = Cart.objects.get_from_request(self.request)
        self.assertIsNotNone(cart, "Cart Object Not Created from request")
        self.assertEqual(cart.user.id, self.user.id, "New Cart Created Belonging to User")

    def test_cart_creation_from_session_key(self):
        """ Test whether cart is created by an unauthenticated User """
        self._run_middleware()
        cart = Cart.objects.get_from_request(self.request)
        self.assertIsNotNone(cart, "Cart Object Not Created from request")
        self.assertIsNotNone(cart.session, "Cart Object has not save the session instance")


class CartModelTestCase(TestCase):
    """ Test the custom methods of my Cart Model """

    @staticmethod
    def _create_test_product(diff='1'):
        return Product.objects.create(
            name='Test Product {}'.format(diff),
            category=Category.objects.create(
                name='Test Category {}'.format(diff),
                slug='test-category-{}'.format(diff)
            ),
            price=Money(250, 'KES'),
            discount_price=Money(200, 'KES'),
        )

    @staticmethod
    def _create_cart():
        return Cart.objects.create(
            user=User.objects.create_user(
                username='john',
                email='johndoe@gmail.com',
                password='password'
            )
        )

    @staticmethod
    def _create_cart_product(cart, product, number):
        return CartProduct.objects.create(
            cart=cart,
            product=product,
            number=number
        )

    def setUp(self):
        # create a product
        self.product = self._create_test_product()

    def test_update_product_number_with_cart_product(self):
        cart = self._create_cart()
        self._create_cart_product(cart, self.product, 2)
        cart_product = cart.update_product_number(self.product.id, 1)
        self.assertEqual(cart_product.number, 1, "Cart update not successful")

    def test_update_product_number_no_cart_product(self):
        cart = self._create_cart()
        with self.assertRaises(NoProductToDelete):
            cart.update_product_number(self.product.id, 0)

    def test_add_product_number_with_cart_product(self):
        cart = self._create_cart()
        self._create_cart_product(cart, self.product, 2)
        cart.add_product(self.product.id, 1)
        cart_product = CartProduct.objects.get(
            cart=cart,
            product_id=self.product.id
        )
        self.assertEqual(
            cart_product.product.id,
            self.product.id,
            "Add Product to Cart was not successfully"
        )

    def test_add_product_number_no_cart_product(self):
        cart = self._create_cart()
        cart.add_product(self.product.id, 0)
        cart_product = CartProduct.objects.get(cart=cart, product_id=self.product.id)
        self.assertEqual(
            cart_product.product.id,
            self.product.id,
            "Add Product to Cart was not successfully"
        )

    def test_remove_product_number_with_cart_product(self):
        cart = self._create_cart()
        self._create_cart_product(cart, self.product, 2)
        cart.remove_product(self.product.id)
        with self.assertRaises(CartProduct.DoesNotExist):
            CartProduct.objects.get(
                cart=cart,
                product_id=self.product.id
            )

    def test_remove_product_number_no_cart_product(self):
        cart = self._create_cart()
        with self.assertRaises(NoProductToDelete):
            cart.remove_product(self.product.id)

    def test_cart_methods(self):
        cart = self._create_cart()
        product1 = self._create_test_product('dan')
        product2 = self._create_test_product('king')
        products_list = [
            {'pk': product1.id, 'number': 5},
            {'pk': product2.id, 'number': 4}
        ]
        # create the cart products
        cart_product1 = CartProduct.objects.create(
            cart=cart,
            product_id=product1.id,
            number=1
        )
        cart_product2 = CartProduct.objects.create(
            cart=cart,
            product_id=product2.id,
            number=1
        )
        # call cart update
        cart.update_cart(products_list)
        # get the updated cart products
        u_cart_product1 = cart.products.get(id=cart_product1.id)
        u_cart_product2 = cart.products.get(id=cart_product2.id)
        msg = "Update Cart Not successful"
        # assert cart has updated successfully
        self.assertEqual(u_cart_product1.number, 5, msg)
        self.assertEqual(u_cart_product2.number, 4, msg)

        # assert number_of_products
        self.assertEqual(
            cart.number_of_products(),
            9,
            "Total Number of Product Not Found"
        )

        # assert cart total price worth
        self.assertEqual(
            cart.total,
            Money(9 * 200, 'KES'),
            "Total Number of Product Not Found"
        )
