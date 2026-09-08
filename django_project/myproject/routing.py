from django.conf import settings


class MyDBRouter:
    """Route each app's models to the database named in ``DATABASE_APPS_MAPPING``.

    Apps that are not listed fall back to the ``default`` database.
    """

    @property
    def _mapping(self):
        return settings.DATABASE_APPS_MAPPING

    def _db_for(self, app_label):
        return self._mapping.get(app_label, 'default')

    def db_for_read(self, model, **hints):
        return self._mapping.get(model._meta.app_label)

    def db_for_write(self, model, **hints):
        return self._mapping.get(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        """Allow a relation only when both objects live in the same database."""
        return self._db_for(obj1._meta.app_label) == self._db_for(obj2._meta.app_label)

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Only migrate an app into the database it is mapped to."""
        return db == self._db_for(app_label)
