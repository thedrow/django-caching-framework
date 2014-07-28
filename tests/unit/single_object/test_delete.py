from unittest import TestCase

from caching_framework.compat import get_cache
from tests.unit.support.models import TestModel

cache = get_cache('objects')


class InvalidateCacheOnDeleteTestCase(TestCase):
    def test_object_is_deleted(self):
        sut = TestModel.objects.create()

        sut.delete()

        self.assertIsNone(sut.pk)
        self.assertFalse(TestModel.objects.filter(pk=sut.pk).exists())

    def test_the_deleted_object_is_not_cached(self):
        sut = TestModel.objects.create()

        key = sut.cache_key
        sut.delete()

        self.assertIsNone(cache.get(key))

