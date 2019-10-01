from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField as BaseField
from phonenumber_field.phonenumber import PhoneNumber as BasePhoneNumber
from phonenumber_field.validators import validate_international_phonenumber


class PhoneNumber(BasePhoneNumber):
    def split(self, string):
        return self.as_international.split(string)


class PhoneNumberField(BaseField):
    attr_class = PhoneNumber
    default_error_messages = {
        'invalid': _('Enter a valid phone number.'),
    }
    default_validators = [validate_international_phonenumber]
