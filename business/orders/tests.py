from rest_framework.reverse import reverse

from client.delivery.models import DeliveryInfo
from utils.tests import TestAuthenticatedUser, unsuccessful_message, TestStaffSuperUser, unauthorised_message
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


class TestUnauthorisedOrderView(TestAuthenticatedUser):
    def setUp(self):
        super().setUp()
        self.order_id = create_order_object(self.user.id)

    def test_retrieve_order_info(self):
        """
        Test the retrieval of  order information
        :return: None
        """
        url = reverse('orders:view_order', kwargs={'pk': self.order_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403, unauthorised_message(response))

    def test_change_order_status(self):
        """
        Test the cancellation of  order data  an cms category
        :return: None
        """
        url = reverse('orders:change_order_status', kwargs={'pk': self.order_id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403, unauthorised_message(response))


class TestAuthorisedOrderView(TestStaffSuperUser):
    def setUp(self):
        super().setUp()
        self.order_id = create_order_object(self.user.id)

    def test_retrieve_order_info(self):
        """
        Test the retrieval of  order information
        :return: None
        """
        url = reverse('orders:view_order', kwargs={'pk': self.order_id})
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            unsuccessful_message(response, "Retrieve Order Information", 200)
        )

    def test_change_order_status(self):
        """
        Test the cancellation of  order data  an cms category
        :return: None
        """
        url = reverse('orders:change_order_status', kwargs={'pk': self.order_id})
        response = self.client.post(url)
        self.assertEqual(
            response.status_code, 200,
            unsuccessful_message(response, "Order Cancellation", 200)
        )
