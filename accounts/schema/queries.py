import graphene

from .types import UserType, UserProfileType


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
