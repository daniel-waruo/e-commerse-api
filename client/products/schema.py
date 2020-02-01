import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from business.products.models import Category, Product,ProductImage
from graphene_django.converter import convert_django_field
from djmoney.models.fields import MoneyField
from pyuploadcare.dj.models import ImageField
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


@convert_django_field.register(ImageField)
def convert_image_group_field(field,registry=None):
    return graphene.String()

@convert_django_field.register(MoneyField)
def convert_image_group_field(field,registry=None):
    return graphene.String()

class CustomNode(relay.Node): 
    class Meta:
        name = 'Node'

    @staticmethod
    def to_global_id(type, id):
        #returns a non-encoded ID
        return id

    @staticmethod
    def get_node_from_global_id(info, global_id, only_type=None):
        model = getattr(Query,info.field_name).field_type._meta.model
        return model.objects.get(id=global_id)

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        # Allow for some more advanced filtering here
        filter_fields = {
            'slug':['exact'],
            'name': ['exact', 'icontains', 'istartswith'],
            'description': ['icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }
        interfaces = (CustomNode,)

class ProductImageType(DjangoObjectType):
    class Meta:
        model  = ProductImage
        fields = ("id","image","product")


class Query(object):
    product = relay.Node.Field(ProductNode)
    all_products = DjangoFilterConnectionField(ProductNode)
    
    product_images = graphene.List(ProductImageType)
    product_image = graphene.Field(ProductImageType)

    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_product_images(self,info,**kwargs):
        return ProductImage.objects.all()