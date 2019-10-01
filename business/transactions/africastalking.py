import africastalking
from django.conf import settings

api_key = settings.AFRICASTALKING_API_KEY
api_product = settings.AFRICASTALKING_API_PRODUCT
api_username = settings.AFRICASTALKING_API_USERNAME


class AfricasTalking:

    def __init__(self):
        africastalking.initialize(api_username, api_key)
        self.pay = africastalking.Payment
        self.sms = africastalking.SMS

    def mobile_checkout(self, phone_number, money):
        response = self.pay.mobile_checkout(
            product_name=api_product,
            phone_number=str(phone_number),
            currency_code=str(money.currency),
            amount=float(money.amount),
            metadata={"agentId": "654", "productId": "4251"},
        )
        return response

    def send_one_sms(self, message, recipient):
        response = self.sms.send(
            message,
            [recipient],
        )
        return response

    def send_bulk_sms(self, message, recipients):
        response = self.sms.send(
            message,
            recipients,
        )
        return response

    def business_to_business_payment(self, business):
        """
        :param business:
        business=dict()
        :return:
        """
        response = self.pay.mobile_b2b(
            api_product,
            business={
                'provider': business['provider'],
                'transferType': business['transfer_type'],
                'currencyCode': business['currency_code'],
                'destinationChannel': business['destination_channel'],
                'destinationAccount': business['destination_account'],
                'amount': business['amount'],
                'metadata': business['metadata']
            }
        )
        return response
