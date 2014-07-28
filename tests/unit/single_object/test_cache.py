from unittest import TestCase

from tests.unit.support.models import TestModel
from caching_framework.compat import get_cache


cache = get_cache('objects')


class CacheObjectTestCase(TestCase):
    def test_object_is_cached(self):
        sut = TestModel.objects.create()
        sut.uncache()

        sut.cache()

        actual = cache.get(sut.cache_key)
        self.assertEqual(actual, sut)

    def test_a_value_error_is_raised_when_the_object_was_not_saved(self):
        sut = TestModel()

        with self.assertRaisesRegexp(ValueError, "Cannot cache an unsaved object"):
            sut.cache()
