from business.authorization.apps import DepartmentAppConfig


class CmsConfig(DepartmentAppConfig):
    label = 'cms'
    name = 'business.products'
    verbose_name = "Products"
