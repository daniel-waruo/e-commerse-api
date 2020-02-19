"""
import all app modules
import all DEPARTMENT_APPS
    check if a Department instance exists
        if it exists
            pass
        else
            create a new department
    get all Department Instances

    exclude the ones belonging to apps in Department Apps
    delete the rest left in the QuerySet
"""

from django.apps import apps
from django.core.management.base import (
    BaseCommand, no_translations,
)
from django.db.models import Q

from business.authorization.apps import DepartmentAppConfig
from business.authorization.models import Department


class Command(BaseCommand):
    help = "Clears unused Department Models"

    @no_translations
    def handle(self, **options):
        # gets a list of all department app configs
        app_configs = apps.get_app_configs()

        # checks if the app config is an instance
        # of Default app config and returns the app_label
        def get_department_app_configs(app_config):
            if isinstance(app_config, DepartmentAppConfig):
                return app_config.label

        # returns a list of app_labels from department app configs
        app_labels = list(map(get_department_app_configs, app_configs))

        # query set of all the department instances without an app label in the app labels list
        queryset = Department.objects.filter(~Q(app_label__in=app_labels))

        if queryset:
            number_deleted = queryset.count()
            queryset.delete()
            self.stdout.write("Process Successful!!\n.Deleted %s Unused Department Model Instances", number_deleted)
        else:
            self.stdout.write("\nNo unused Department Models Instances")
