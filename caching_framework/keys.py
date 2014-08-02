from django.utils.functional import cached_property


class CacheKey(object):
    def __init__(self, namespace, field_names_and_values):
        self.namespace = namespace
        self.field_names_and_values = field_names_and_values

    def __str__(self):
        fields_cache_fragment = ';'.join(['{0}={1}'.format(field_name, value) for field_name, value in self.field_names_and_values])
        return '{0.namespace}:{fields_cache_fragment}'.format(self, fields_cache_fragment=fields_cache_fragment)


class CacheKeysGenerator(object):
    def __init__(self, model):
        self.model = model

    @cached_property
    def object_cache_keys(self):
        unique_field_names, unique_for_date_field_names = self.model._get_unique_checks()
        namespace = self.model._meta.db_table

        unique_fields = []
        for _, field_names in unique_field_names:
            unique_fields.append(
                [(field_name, getattr(self.model, field_name)) for field_name in
                 field_names])

        for _, __, field_name, unique_for_date_field in unique_for_date_field_names:
            unique_fields.append([(field_name, getattr(self.model, field_name)), (unique_for_date_field, getattr(self.model, unique_for_date_field))])

        unique_fields.append([('pk', self.model.pk)])

        return (str(CacheKey(namespace, fields)) for fields in unique_fields)