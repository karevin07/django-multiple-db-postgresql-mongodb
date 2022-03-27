import random

from django.db import connections

from .multiple_db_settings import DATABASE_APPS_MAPPING


class MyDBRouter:

    router_mappings = DATABASE_APPS_MAPPING

    user_app_labels = {'auth', 'contenttypes', 'admin', 'sessions', 'example_user'}
    app_app_labels = {'example_app'}


    user_db = connections[router_mappings['example_user']]
    app_db = connections[router_mappings['example_app']]

    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.router_mappings:
            return connections[self.router_mappings[model._meta.app_label]]
        else:
            return False

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.router_mappings:
            return connections[self.router_mappings[model._meta.app_label]]
        else:
            return False

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
                obj1._meta.app_label in self.router_mappings or
                obj2._meta.app_label in self.router_mappings
        ):
            return True
        else:
            print(f"no database {obj1._meta.app_label}")
            print(f"no database {obj2._meta.app_label}")
            return False


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print(db, app_label, model_name)
        """
        All non-auth models end up in this pool.
        """
        if db == 'default':
            if app_label in self.user_app_labels:
                return True
            else:
                return None
        elif db == 'mongo_data':
            if app_label in self.app_app_labels:
                return True
            else:
                return None
        else:
            return False
        # return None