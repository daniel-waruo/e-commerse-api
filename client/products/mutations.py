import graphene

from .models import ProductReview
from .types import ProductReviewType


class CreateReview(graphene.Mutation):
    """Create a new class"""
    review = graphene.Field(ProductReviewType)

    """Define the data to be sent ot the server"""

    class Arguments:
        product_id = graphene.String(required=True)

        text = graphene.String(required=True)

        rating = graphene.Int(required=True)

    """Save the data sent by the user to the db"""

    def mutate(self, info, **kwargs):
        # get request object
        request = info.context
        # check if user is authenticated
        if request.user.is_authenticated:
            # check if product review is already created
            if ProductReview.objects.filter(product_id=kwargs['product_id'], user=request.user):
                # raise exception if a product review is found
                raise Exception("A user is limited to only one review")
            # create an instance of Product Review as review
            review = ProductReview(
                product_id=kwargs['product_id'],
                user=request.user,
                rating=kwargs['rating'],
            )
            # save review in database
            review.save()
            # return the newly created data
            return CreateReview(
                review=review
            )
        # if user is not authenticated raise an exception
        raise Exception("Login to review product")


class Mutation(graphene.ObjectType):
    create_product_review = CreateReview.Field()
