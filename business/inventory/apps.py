from business.authorization.apps import DepartmentAppConfig


class InventoryConfig(DepartmentAppConfig):
    label = 'inventory'
    name = 'business.inventory'
    verbose_name = 'Inventory Management'
