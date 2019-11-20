from business.authorization.apps import DepartmentAppConfig


class CmsConfig(DepartmentAppConfig):
    label = 'cms'
    name = 'business.cms'
    verbose_name = "Content Management System"
