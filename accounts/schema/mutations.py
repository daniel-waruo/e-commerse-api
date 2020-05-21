import graphene

from .types import UserType
from ..serializers import UserEditSerializer


class UserEditMutation(graphene.Mutation):
    """
      Edit User Information Mutation
      This class is used to edit information
      that a user has provided in the application
      The args to be placed in mutation are:-

    """
    user = graphene.Field(UserType)

    errors = graphene.JSONString()

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        gender = graphene.String()

    def mutate(self, info, **kwargs):
        request = info.context
        if request.user.is_authenticated:
            serializer = UserEditSerializer(instance=request.user, data=kwargs, context=request)
            if serializer.is_valid():
                user = serializer.save()
                return UserEditMutation(user=user)
            return UserEditMutation(errors=serializer.errors)
        # if user is not authenticated raise an exception
        raise Exception("Login to edit User Information")


class Mutation(graphene.ObjectType):
    edit_user_information = UserEditMutation.Field()
    edit_user_mutation = UserEditMutation.Field()
