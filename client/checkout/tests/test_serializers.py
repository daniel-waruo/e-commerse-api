from django.contrib.auth import get_user_model
from django.test import TestCase

from ..serializers import OrderQuotationSerializer

User = get_user_model()


class OrderQuotationSerializerTestCase(TestCase):

    def setUp(self):
        self.data = {
            'name': 'Daniel Waruo King\'ang\'ai',
            'email': 'johndoe@gmail.com',
            'phone_number': '+254722483461',
            'location_name': 'Test Location',
            'location_description': 'Test Location Description',
            'lat': '-1.2206014',
            'long': '36.8944205'
        }
        self.serializer = OrderQuotationSerializer(data=self.data)

    def test_get_quotaiton(self):
        if self.serializer.is_valid():
            sendy_data = self.serializer.save()
            self.assertIsNotNone(sendy_data)
            raise Exception(sendy_data)
