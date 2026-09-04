from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from django.db.models.fields.json import JSONField
        _original_from_db_value = JSONField.from_db_value

        def safe_from_db_value(self, value, expression, connection):
            if value is None or isinstance(value, (dict, list)):
                return value
            return _original_from_db_value(self, value, expression, connection)

        JSONField.from_db_value = safe_from_db_value
