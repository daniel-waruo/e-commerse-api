from rest_framework.reverse import reverse

from business.delivery.models import DeliveryInfo
from utils.tests import UserTestCase
from .models import Order


def create_delivery_object(user_id):
    delivery_info = DeliveryInfo(
        user_id=user_id,
        phone_number="+254797792447",
        email="test@gmail.com"
    )
    delivery_info.save()
    return delivery_info.id


def create_order_object(user_id):
    create_delivery_object(user_id)
    order = Order(
        user_id=user_id,
        delivery_info_id=1
    )
    order.save()
    return order.id


class TestOrderView(UserTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)
        self.order_id = create_order_object(self.user.id)

    def test_retrieve_order_info(self):
        """
        Test the retrieval of  product data  an cms category
        :return: None
        """
        self.client.login(username="test", password="test")
        url = reverse('orders:view_order', kwargs={'pk': self.order_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200,
                         'Retrieve Order is not Successful.\n'
                         'Expected  Response Code 200, received {0} instead with content as :-'
                         '\n\t {1}.'
                         .format(response.status_code, response.content))
