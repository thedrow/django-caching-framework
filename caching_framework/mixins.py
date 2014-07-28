from django.utils.functional import cached_property

from caching_framework.compat import get_cache
from caching_framework.utils import generate_cache_key


objects_cache = get_cache('objects')


class CachingMixin(object):
    @cached_property
    def cache_key(self):
        return generate_cache_key(self)

    def cache(self):
        if not self.pk is None:
            raise ValueError("Cannot cache an unsaved object")

        objects_cache.set(self.cache_key, self)

    def uncache(self):
        if self.pk is None:
            raise ValueError("Cannot uncache an unsaved object")

        objects_cache.delete(self.cache_key)

    @classmethod
    def invalidate(cls, pk):
        try:
            obj = cls.objects.get(pk=pk)
            obj.cache()
        except cls.DoesNotExist:
            obj = cls(pk=pk)
            obj.uncache()
