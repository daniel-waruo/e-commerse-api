import graphene
from graphene_django.converter import convert_django_field
from pyuploadcare.dj.models import ImageField
import client.products.schema
import client.web.schema

class Query(client.products.schema.Query,client.web.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
