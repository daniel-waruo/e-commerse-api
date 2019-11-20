from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
@receiver(post_save, sender=User)
def create_profile(**kwargs):
    if kwargs['created']:
        UserProfile.objects.create(user=kwargs['instance'])


STAFF_TYPES = (
    (0, "Department Staff"),
    (1, "Department Manager"),
    (2, "General Manager")
)


class StaffUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    departments = models.ManyToManyField(to=Department)
    staff_type = models.PositiveSmallIntegerField(choices=STAFF_TYPES)

    def __str__(self):
        return self.user.username

    def save(self, **kwargs):
        user = super().save(**kwargs)
        return user


@receiver(post_save, sender=StaffUser)
def give_permissions(**kwargs):
    staff_user = kwargs["instance"]
    if staff_user.staff_type == 1:
        from business.authorization.utils import set_department_manager_perms
        department_ids = list(map(
            lambda department: department.id,
            staff_user.departments.all()
        ))
        set_department_manager_perms(staff_user.user.id, department_ids)
    elif staff_user.staff_type == 2:
        from business.authorization.utils import set_general_manager_perms
        department_ids = list(map(
            lambda department: department.id,
            staff_user.departments.all()
        ))
        set_general_manager_perms(staff_user.user.id, department_ids)
