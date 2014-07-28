import random

from django.test import TransactionTestCase

from caching_framework.compat import get_cache
from tests.unit.support.models import TestModel


objects_cache = get_cache('objects')


class DeleteManyObjectsTestCase(TransactionTestCase):
    def test_deleting_all_objects_invalidates_the_entire_cache(self):
        objects = [TestModel.objects.create(bar=1) for _ in range(10)]

        TestModel.objects.all().delete()

        expected = set(TestModel.objects.all())
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)

    def test_deleting_some_objects_invalidates_the_cache(self):
        objects = filter(lambda o: o.bar == 1,
                         [TestModel.objects.create(bar=random.choice((1, 2))) for _ in range(10)])

        TestModel.objects.filter(bar=1).delete()

        expected = set(TestModel.objects.filter(bar=1))
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)
