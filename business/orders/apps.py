from business.authorization.apps import DepartmentAppConfig


class OrdersConfig(DepartmentAppConfig):
    name = 'business.orders'
    verbose_name = 'Order Management'
    label = 'orders'
