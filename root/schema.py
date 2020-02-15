import graphene

from accounts.schema import Query as UserQuery
from client.cart.schema import Query as CartQuery
from client.products.schema import Query as ProductQuery
from client.web.schema import Query as WebQuery


class Query(ProductQuery, WebQuery, CartQuery, UserQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
