from unittest import TestCase
from caching_framework.utils import generate_cache_key
from tests.unit.support.models import TestModel


class GenerateHashKeyTestCase(TestCase):
    def test_raise_value_error_for_unsaved_objects(self):
        obj = TestModel()

        with self.assertRaisesRegexp(ValueError, "Cannot generate a cache key for an unsaved object"):
            generate_cache_key(obj)

    def test_cache_key_is_generated_correctly(self):
        obj = TestModel.objects.create()
        expected = '%s:%s' % (obj._meta.db_table, obj.pk)

        actual = generate_cache_key(obj)

        self.assertEqual(expected, actual)
