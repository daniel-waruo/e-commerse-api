from business.authorization.apps import DepartmentAppConfig


class ProductsConfig(DepartmentAppConfig):
    label = 'products'
    name = 'business.products'
    verbose_name = "Products"
