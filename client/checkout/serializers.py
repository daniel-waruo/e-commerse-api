from django.core.exceptions import ImproperlyConfigured
from rest_framework import serializers
from django.conf import settings
from business.orders.models import Order
from client.delivery.models import DeliveryInfo
from sendy_it import SendyIT, Person, Location, Delivery

from phonenumber_field.serializerfields import PhoneNumberField

# inititalize the sendy object
# TODO:write a django application to
sendy = SendyIT(
    api_key=settings.SENDY_API_KEY,
    username=settings.SENDY_USERNAME
)


class CheckOutSerializer(serializers.Serializer):
    """ Handles the Checkout and changes

    Handle the change from a cart to and order
    """
    sendy_order_no = serializers.CharField()
    delivery_info_id = serializers.PrimaryKeyRelatedField(queryset=DeliveryInfo.objects.all())

    def validate(self, attrs):
        """validate data """
        if not self.context.user.is_authenticated:
            raise serializers.ValidationError("User Must Be authenticated")
        return attrs

    def validate_info_id(self, value):
        user = self.context.user
        if not user.delivery_contacts.all().exists():
            raise serializers.ValidationError(detail='User Has No Saved Delivery Contacts')
        if not user.delivery_contacts.filter(id=value).exists():
            raise serializers.ValidationError(detail='No Such Delivery Contact is Saved')
        return value

    def create(self, validated_data):
        """Create an Order From The Cart and return It"""
        cart = self.context.user.cart
        return Order.objects.create_from_cart(
            cart=cart,
            delivery_info=DeliveryInfo.objects.get(id=validated_data['delivery_info_id']),
            sendy_order_no=validated_data['sendy_order_no']
        )

    def update(self, instance, validated_data):
        pass

    def save(self, **kwargs):
        return self.create(self.validated_data)


class OrderQuotationSerializer(serializers.Serializer):
    """Handles Getting The Price Quotation for the Application

    Args:
        name - name of the person to be contacted for the delivery
        email - email of the person to be contacted for the package
        phone_number - phone number of the contact person
        location_name - name or address of the area we are delivering to
        location_description - description of the area we are delivering to
        lat - latitude of the area we are delivering to
        long - longitude of the area we are delivering to
    """

    name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone_number = PhoneNumberField(required=True)
    location_name = serializers.CharField(required=True)
    location_description = serializers.CharField(required=True)
    lat = serializers.FloatField(required=True)
    long = serializers.FloatField(required=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        sendy.get_delivery_quote(
            recipient=Person(
                name=validated_data['name'],
                email=validated_data['email'],
                phone=str(validated_data['phone_number']),
                type='recepient'
            ),
            to_location=Location(
                name=validated_data['location_name'],
                lat=validated_data['lat'],
                long=validated_data['long'],
                description=validated_data['location_description'],
                type='to'
            ),
            sender=Person(
                **settings.SENDY_SENDER_DETAILS,
                type='sender'
            ),
            from_location=Location(
                **settings.SENDY_LOCATION_DETAILS,
                type='from'
            )
        )

    def save(self, **kwargs):
        return self.create(self.validated_data)
