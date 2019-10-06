import datetime

from client.cart.models import Cart, CartProduct
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.utils import timezone
