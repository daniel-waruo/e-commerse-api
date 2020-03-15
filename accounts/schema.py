import graphene
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField

from .models import User, UserProfile


# This is configured in the CategoryNode's Meta class (as you can see below)
class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ['password']


@convert_django_field.register(ImageField)
def convert_field(field, registry=None):
    return graphene.String()


class UserProfileType(DjangoObjectType):
    class Meta:
        model = UserProfile


class Query(graphene.ObjectType):
    user = graphene.Field(UserType)
    user_profile = graphene.Field(UserProfileType)

    def resolve_user(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user
        return None

    def resolve_user_profile(self, info):
        user = info.context.user
        if user.is_authenticated:
            return user.userprofile
        return None
