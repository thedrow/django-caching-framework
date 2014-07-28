from django.db.models.deletion import Collector
from django.db.models.query import QuerySet
from django.db.models.query_utils import deferred_class_factory
from caching_framework.compat import get_cache

objects_cache = get_cache('objects')


class CachingQuerySetMixin(object):
    def __init__(self, **kwargs):
        super(CachingQuerySetMixin, self).__init__(**kwargs)
        self._pks = []

    def _invalidate_objects_by_pk(self, *args):
        if args:
            fields = self.model._meta.get_all_field_names()
            fields.remove(self.model._meta.pk.name)
            model = deferred_class_factory(self.model, fields)
            objects = {}
            for pk in args:
                obj = model(pk=pk)
                objects[obj.cache_key] = obj

            objects_cache.set_many(objects)

    def _invalidate_objects_by_query(self, **kwargs):
        if kwargs:
            objects = self.model._base_manager.filter(**kwargs).only('pk')
            objects_cache.set_many({obj.cache_key: obj for obj in objects})

    def _invalidate_objects(self, *args):
        if args:
            objects_cache.set_many({obj.cache_key: obj for obj in args})

    def _uncache_current_objects(self):
        objects = self.only('pk')
        objects_cache.delete_many([obj.cache_key for obj in objects])

    def update(self, **kwargs):
        rows = super(CachingQuerySetMixin, self).update(**kwargs)

        if self._pks:
            self._invalidate_objects_by_pk(*self._pks)
        else:
            self._invalidate_objects_by_query(**kwargs)

        return rows

    def filter(self, *args, **kwargs):
        qs = super(CachingQuerySetMixin, self).filter(*args, **kwargs)

        pk_name = '%s__in' % self.model._meta.pk.name
        query_args = kwargs.keys()
        if len(kwargs.keys()) == 1:
            # When the filtering was done by the primary key there is no need to perform another query in order to
            # invalidate the cache. The query will be performed by the cache backend later on.
            if 'pk__in' in query_args:
                self._pks = kwargs['pk__in']
                qs._pks = kwargs['pk__in']
            elif pk_name in query_args:
                self._pks = kwargs[pk_name]
                qs._pks = kwargs[pk_name]
        elif len(kwargs.keys()) == 2 and 'pk__in' in query_args and pk_name in query_args:
            # This is an optimization to a very unlikely edge case but because Django allows it there is no reason
            # to perform another query for it.
            qs._pks = set(kwargs[pk_name]).union(set(kwargs['pk__in']))

        return qs

    def delete(self):
        self._invalidate_objects_by_query()
        super(CachingQuerySetMixin, self).delete()

    def bulk_create(self, objs, batch_size=None):
        objects = tuple(objs)
        objs = super(CachingQuerySetMixin, self).bulk_create(objs, batch_size=batch_size)

        self._invalidate_objects(*filter(lambda o: o.pk is not None, objects))

        objects_pending_invalidation = filter(lambda o: not o.pk, objects)
        for obj in objects_pending_invalidation:
            kwargs = {field.name: getattr(obj, field.name) for field in obj._meta.fields}
            kwargs.pop('id', None)
            self._invalidate_objects_by_query(**kwargs)

        return objs

    def get(self, *args, **kwargs):
        pk_name = self.model._meta.pk.name
        pk_name_in = '%s__in' % pk_name
        pk_name_exact = '%s__exact' % pk_name
        query_args = kwargs.keys()
        if len(kwargs.keys()) == 1:
            if 'pk__in' in query_args and len(kwargs['pk__in']) == 1:
                pk = kwargs['pk__in'][0]
            elif 'pk' in query_args:
                pk = kwargs['pk']
            elif 'pk__exact' in query_args:
                pk = kwargs['pk__exact']
            elif pk_name_in in query_args and len(kwargs[pk_name_in]) == 1:
                pk = kwargs[pk_name_in][0]
            elif pk_name in query_args:
                pk = kwargs[pk_name]
            elif pk_name_exact in query_args:
                pk = kwargs[pk_name_exact]

            model = self.model(pk=pk)
            obj = objects_cache.get(model.cache_key)

            if obj:
                return obj

        return super(CachingQuerySetMixin, self).get(*args, **kwargs)

    def clone(self):
        qs = super(CachingQuerySetMixin, self).clone()
        qs._pks = self._pks

        return qs


class CachingQuerySet(CachingQuerySetMixin, QuerySet):
    pass
