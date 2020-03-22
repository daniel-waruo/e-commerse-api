import graphene
from rest_framework.exceptions import ValidationError

from .types import UserType
from ..serializers import UserInformationSerializer


class EditUserInformation(graphene.Mutation):
    """
      Edit User Information Mutation
      This class is used to edit information
      that a user has provided in the application
      The args to be placed in mutation are:-

    """
    user = graphene.Field(UserType)

    """Define the data to be sent ot the server"""

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        gender = graphene.String()

    """Save the data sent by the user to the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            # call user information serializer
            serializer = UserInformationSerializer(data=kwargs)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save(request.user)
                # return the newly created data
                return EditUserInformation(
                    user=user
                )
        # if user is not authenticated raise an exception
        raise ValidationError("Login to edit User Information")


class Mutation(graphene.ObjectType):
    edit_user_information = EditUserInformation.Field()
