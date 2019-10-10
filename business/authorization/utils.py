from django.apps import AppConfig
from client.cart.errors import BadConfigError
from django.db.utils import OperationalError


class DepartmentAppConfig(AppConfig):
    """
    Department App Config is a app configuration that allow for the creation
    of departments
    """

    def __init__(self, app_name, app_module):
        if not self.label:
            raise BadConfigError("Label Must be explicitly set for Department App Configurations")
        super().__init__(app_name, app_module)

    def ready(self):
        from .models import Department
        # get query ser with app_label
        queryset = Department.objects.filter(app_label=self.label)
        # if queryset check is verbose name is same

        try:
            if queryset:
                # check is the verbose name has changed
                if not queryset.filter(name=self.verbose_name):
                    queryset.get(app_label=self.label).save(name=self.verbose_name)
            else:
                Department.objects.create(
                    name=self.verbose_name,
                    app_label=self.label
                )
        except OperationalError:
            pass
