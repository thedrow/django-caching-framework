from unittest import TestCase

from caching_framework.compat import get_cache
from tests.unit.support.models import TestModel


cache = get_cache('objects')


class InvalidateCacheOnSaveTestCase(TestCase):
    def test_object_is_saved(self):
        sut = TestModel()

        sut.save()

        self.assertIsNotNone(sut.pk)
        self.assertTrue(TestModel.objects.filter(pk=sut.pk).exists())

    def test_an_object_is_cached(self):
        sut = TestModel()

        sut.save()

        self.assertIsNotNone(cache.get(sut.cache_key))

    def test_the_saved_object_is_cached(self):
        sut = TestModel()

        sut.save()

        actual = cache.get(sut.cache_key)
        self.assertEqual(actual, sut)
