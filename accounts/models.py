from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from pyuploadcare.dj.models import ImageField

from business.authorization.models import Department
from utils.geo.phone_numbers.fields import PhoneNumberField

# Create your models here.

# These are gender choices available

gender_choices = (
    ('m', 'MALE'),
    ('f', 'FEMALE'),
    ('u', 'UNKNOWN'),
)


class User(AbstractUser):
    """
    Custom User Class
    """
    email = models.EmailField(
        unique=True,
        null=False,
        error_messages={
            'unique': _("The email is already in use"),
        },
    )

    def get_email(self):
        # function for getting email address
        return self.email


class UserProfile(models.Model):
    """
    Models for the User Profile
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


# create a user profile instance as soon as the user has been created

def create_profile(**kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


class StaffUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    departments = models.ManyToManyField(to=Department)

    def __str__(self):
        return self.user.username


"""
 TODO:
    # Implement Permissions and Privileges     
"""
post_save.connect(create_profile, sender=User)
