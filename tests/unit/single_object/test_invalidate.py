from unittest import TestCase

from tests.unit.support.models import TestModel
from caching_framework.compat import get_cache


objects_cache = get_cache('objects')


class InvalidationTestCase(TestCase):
    def test_invalidate_existing_object(self):
        obj = TestModel.objects.create()
        obj.uncache()

        TestModel.invalidate(obj.pk)

        actual = objects_cache.get(obj.cache_key)
        self.assertEqual(actual, obj)

    def test_invalidate_deleted_object(self):
        obj = TestModel.objects.create()
        pk = obj.pk
        cache_key = obj.cache_key
        obj.delete()
        objects_cache.set(cache_key, obj)

        TestModel.invalidate(pk)

        actual = objects_cache.get(obj.cache_key)
        self.assertIsNone(actual)
