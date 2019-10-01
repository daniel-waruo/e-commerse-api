import decimal
from country_currencies import get_by_country
from djmoney.contrib.exchange.models import convert_money
from djmoney.money import Money
from ipware import get_client_ip
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
import geoip2.errors

BASE_CURRENCY = settings.BASE_CURRENCY


def get_currency_from_ip(request):
    ip, is_r = get_client_ip(request)
    if ip is None:
        return BASE_CURRENCY
    else:
        g = GeoIP2()
        try:
            country_code = g.city(ip)["country_code"]
        except geoip2.errors.AddressNotFoundError:
            return BASE_CURRENCY
        else:
            currency = get_by_country(country_code, default=BASE_CURRENCY)
            return currency[0]


def round_off(money):
    rounded = round(money.amount, 2)
    amount = decimal.Decimal(rounded).quantize(
        decimal.Decimal('0.00'),
        rounding=decimal.ROUND_UP
    )
    return Money(amount, money.currency)


def change_currency(money_object, currency_code):
    return convert_money(money_object, currency_code)


def translate_money(request, money):
    currency = request.COOKIES.get('currency')
    if currency is None:
        currency = get_currency_from_ip(request)
    return change_currency(money, currency)
