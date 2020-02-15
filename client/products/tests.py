from rest_framework.reverse import reverse

from client.delivery.models import DeliveryInfo
from utils.tests import UserTestCase


class TestCreateDeliveryInfo(UserTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)
        create_delivery_info_object(self.user.id)

    def test_create_delivery_info(self):
        self.client.login(username="test", password="test")
        url = reverse("delivery:add_delivery_info")
        response = self.client.post(url, {
            "phone_number": "+254797792447",
            "email": "test@gmail.com"
        })
        self.assertEqual(response.status_code, 201,
                         'Delivery Info  not Created.Expected Response Code 201, received {0} instead.'
                         'It returned \n{1}'
                         .format(response.status_code, response.content))


def create_delivery_info_object(user_id):
    delivery = DeliveryInfo(
        user_id=user_id,
        phone_number="+254797792447",
        email="test@gmail.com",
    )
    delivery.save()
    return delivery


class TestDeliverInfoView(UserTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_login(user=self.user)
        self.client.force_authenticate(user=self.user, token=self.token)
        create_delivery_info_object(self.user.id)

    def test_retrieve_delivery_info(self):
        url = reverse(
            "delivery:delivery_info",
            kwargs={"pk": 1}
        )

        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            'Delivery Info  not Retrieved.Expected Response Code 200, received {0} instead.'
            'It returned \n{1}'.format(response.status_code, response.content)
        )

    def test_update_delivery_info(self):
        self.client.login(username="test", password="test")
        url = reverse(
            "delivery:delivery_info",
            kwargs={"pk": 1}
        )
        response = self.client.put(url, {
            "phone_number": "+254797792447",
            "email": "testupdate@gmail.com"
        })
        self.assertEqual(
            response.status_code, 200,
            'Delivery Info  not Updated.Expected Response Code 200, received {0} instead.'
            'It returned \n{1}'.format(response.status_code, response.content)
        )

    def test_delete_delivery_info(self):
        self.client.login(username="test", password="test")
        url = reverse(
            "delivery:delivery_info",
            kwargs={"pk": 1}
        )
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, 204,
            'Delivery Info  not Deleted.Expected Response Code 204, received {0} instead.'
            'It returned \n{1}'.format(response.status_code, response.content)
        )

    def test_list_delivery_info(self):
        self.client.login(username="test", password="test")
        url = reverse("delivery:list_delivery_info")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, 200,
            'Delivery Info  not Listed.Expected Response Code 200, received {0} instead.'
            'It returned \n{1}'.format(response.status_code, response.content)
        )
