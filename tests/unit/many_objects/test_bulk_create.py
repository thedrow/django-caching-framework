from django.test import TransactionTestCase

from caching_framework.compat import get_cache
from tests.unit.support.models import TestModel


objects_cache = get_cache('objects')


class CreateManyObjectsTestCase(TransactionTestCase):
    def test_creating_objects_in_bulk_with_no_primary_keys_invalidates_the_entire_cache(self):
        objects = [TestModel(bar=100) for _ in range(10)]

        TestModel.objects.bulk_create(objects)

        expected = set(TestModel.objects.filter(bar=100))
        actual = set(objects_cache.get_many([obj.cache_key for obj in expected]).values())

        self.assertEqual(actual, expected)

    def test_creating_objects_in_bulk_with_primary_keys_invalidates_the_entire_cache(self):
        objects = [TestModel(pk=pk, bar=100) for pk in range(10)]

        TestModel.objects.bulk_create(objects)

        expected = set(TestModel.objects.filter(bar=100))
        actual = set(objects_cache.get_many([obj.cache_key for obj in expected]).values())

        self.assertEqual(actual, expected)