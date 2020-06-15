from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money
from sendy_it import SendyIT, Person, Location
from business.orders.models import Order
from client.cart.models import Cart, CartProduct
from business.products.models import Product, Category
from client.delivery.models import DeliveryInfo
from django.conf import settings

User = get_user_model()


class OrderTestCase(TestCase):

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

    @staticmethod
    def _create_delivery_info(user):
        return DeliveryInfo.objects.create(
            user=user,
            phone_number="+254792384567",
            email='johndoe@heavenishome.com'
        )

    @staticmethod
    def _get_order_no():
        api_key = settings.SENDY_API_KEY
        api_username = settings.SENDY_USERNAME
        sendy = SendyIT(api_key, api_username)
        # details of the person who is receiving the package
        recipient = Person(
            name='John Doe King',
            phone='0722180542',
            email='johndoe@gmail.com',
            type='recepient'
        )

        # details of the person who is sending the package
        sender = Person(
            name="Jane King Doe",
            phone="0797792447",
            email="sendyer@gmail.com",
            type='sender',
            sender_notes="Sender specific notes"
        )

        # location from where the package will be received
        from_location = Location(
            name='Lavington',
            lat='-1.26869',
            long='36.885',
            description='home',
            type='from'
        )

        # location where the package will be delivered to
        to_location = Location(
            name='Green House',
            lat='-1.385',
            long='36.489',
            description='office',
            type='to'
        )
        response_data = sendy.get_delivery_quote(
            recipient=recipient,
            sender=sender,
            to_location=to_location,
            from_location=from_location
        )
        return response_data['data']['order_no']

    def setUp(self) -> None:
        self.cart = self._create_cart()
        self.product = self._create_test_product()
        self.cart_product = self._create_cart_product(self.cart, self.product, 3)
        self.order_no = self._get_order_no()
        self.delivery_info = self._create_delivery_info(self.cart.user)

    def test_create_from_cart_with_order_no(self):
        """Tests the Creation of an Order using the Cart"""
        order = Order.objects.create_from_cart(
            self.cart,
            self.delivery_info,
            self.order_no
        )
        self.assertIsNotNone(order.products.all())
        self.assertIs(order.state, "pending")

    def test_create_from_cart_without_order_no(self):
        """Test the Creation of an Order from a Cart without providing the Sendy Order No """
        order = Order.objects.create_from_cart(
            self.cart,
            self.delivery_info,
            self.order_no
        )
        recipient = Person(
            name='John Koe King',
            phone='0724180542',
            email='johndode@gmail.com',
            type='recepient'
        )

        # details of the person who is sending the package
        sender = Person(
            name="Jane jing Doe",
            phone="0796792447",
            email="sendyser@gmail.com",
            type='sender',
            sender_notes="Sender very specific notes"
        )

        # location from where the package will be received
        from_location = Location(
            name='Lavington',
            lat='-1.26869',
            long='36.884',
            description='school',
            type='from'
        )

        # location where the package will be delivered to
        to_location = Location(
            name='Green House',
            lat='-1.385',
            long='36.489',
            description='office',
            type='to'
        )
        order.request_delivery(
            to_location=to_location,
            from_location=from_location,
            sender=sender,
            recipient=recipient,
            quote=True
        )
        self.assertIsNotNone(order.products.all())
        self.assertIs(order.state, "pending")

    def test_deliver_order(self):
        """Testing Whether One can deliver an Order"""
        order = Order.objects.create_from_cart(
            self.cart,
            self.delivery_info,
            self.order_no
        )
        # deliver the order
        order.complete_order()
        self.assertIsNotNone(order)
        self.assertIs(order.state, "shipping")

    def test_cancel_order(self):
        order = Order.objects.create_from_cart(
            self.cart,
            self.delivery_info,
            self.order_no
        )
        # ask for delivery then cancel the order
        order.complete_order()
        order.cancel_order()
        self.assertIsNotNone(order)
        self.assertIs(order.state, "cancelled")

    def test_complete_order(self):
        order = Order.objects.create_from_cart(
            self.cart,
            self.delivery_info,
            self.order_no
        )
        # if the order ID is available complete the order
        # if only the rates were affected
        order.complete_order()
        self.assertIsNotNone(order)
        self.assertIs(order.state, "shipping")
