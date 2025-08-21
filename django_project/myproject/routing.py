import random

from .multiple_db_settings import DATABASE_APPS_MAPPING


class MyDBRouter:
    router_mappings = DATABASE_APPS_MAPPING

    user_app_labels = ['auth', 'contenttypes', 'admin', 'sessions', 'example_user']
    app_app_labels = ['example_app']

    def db_for_read(self, model, **hints):

        if model._meta.app_label in self.router_mappings:
            return self.router_mappings[model._meta.app_label]
        else:
            return False

    def db_for_write(self, model, **hints):

        if model._meta.app_label in self.router_mappings:
            return self.router_mappings[model._meta.app_label]
        else:
            return False

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if ob1 and ob2 is involved
        """
        if (
                obj1._meta.app_label in self.router_mappings or
                obj2._meta.app_label in self.router_mappings
        ):
            return True
        else:
            return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the user model appears in the default db
        """
        if app_label in self.router_mappings:
            return db == self.router_mappings[app_label]
        return db == 'default'
