import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from ..models import User, UserProfile


# This is configured in the CategoryNode's Meta class (as you can see below)
class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile
