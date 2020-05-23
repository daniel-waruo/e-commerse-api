from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from pyuploadcare.dj.models import ImageField

from utils.phone_number_field import PhoneNumberField

# Create your models here.

# These are gender choices available

gender_choices = (
    ('m', 'MALE'),
    ('f', 'FEMALE'),
    ('u', 'UNKNOWN'),
)


class User(AbstractUser):
    """Custom User Model"""
    email = models.EmailField(
        unique=True,
        null=False,
        error_messages={
            'unique': _("The email is already in use"),
        },
    )


class UserProfile(models.Model):
    """ User Profile Model
    This model stores information that is not mandatory to acquire a user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    gender = models.CharField(max_length=1, choices=gender_choices, default='u', null=True)
    location = models.CharField(max_length=100, default='', null=True)
    phone_number = PhoneNumberField(null=True)
    image = ImageField(null=True)
    birth_day = models.DateField(null=True)
    bio_data = models.TextField(null=True)

    def __str__(self):
        return self.user.__str__()

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_profile(**kwargs):
    """Create a User Profile instance after a user instance has been created """
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])
