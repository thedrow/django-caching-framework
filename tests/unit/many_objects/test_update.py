from django.test import TransactionTestCase

from caching_framework.compat import get_cache
from tests.unit.support.models import TestModel


objects_cache = get_cache('objects')


class UpdateManyObjectsTestCase(TransactionTestCase):
    def test_when_updating_many_objects_while_filtering_by_pk_the_objects_cache_is_invalidated(self):
        objects = [TestModel.objects.create() for _ in range(10)]
        pks = [obj.pk for obj in objects]

        TestModel.objects.filter(pk__in=pks).update(bar=2)

        expected = set(TestModel.objects.filter(pk__in=pks))
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)

    def test_when_updating_many_objects_while_filtering_by_id_the_objects_cache_is_invalidated(self):
        objects = [TestModel.objects.create() for _ in range(10)]
        pks = [obj.pk for obj in objects]

        TestModel.objects.filter(id__in=pks).update(bar=2)

        expected = set(TestModel.objects.filter(pk__in=pks))
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)

    def test_when_updating_many_objects_while_filtering_both_by_id_and_pk_the_objects_cache_is_invalidated(self):
        objects = [TestModel.objects.create() for _ in range(10)]
        pks = [obj.pk for obj in objects]

        TestModel.objects.filter(id__in=pks, pk__in=pks[:5]).update(bar=2)

        expected = set(TestModel.objects.filter(pk__in=pks))
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)

    def test_when_updating_many_objects_while_filtering_by_attribute_the_objects_cache_is_invalidated(self):
        objects = [TestModel.objects.create(bar=1) for _ in range(10)]
        pks = [obj.pk for obj in objects]

        TestModel.objects.filter(bar=1).update(bar=2)

        expected = set(TestModel.objects.filter(pk__in=pks))
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)

    def test_when_updating_many_objects_while_filtering_by_both_attribute_and_pk_the_objects_cache_is_invalidated(self):
        objects = [TestModel.objects.create(bar=1) for _ in range(10)]
        pks = [obj.pk for obj in objects]

        TestModel.objects.filter(bar=1, pk__in=pks).update(bar=2)

        expected = set(TestModel.objects.filter(pk__in=pks))
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)

    def test_when_updating_all_objects_the_objects_cache_is_invalidated(self):
        TestModel._base_manager.all().delete()
        objects = [TestModel.objects.create(bar=1) for _ in range(10)]

        TestModel.objects.update(bar=2)

        expected = set(TestModel.objects.all())
        actual = set(objects_cache.get_many([obj.cache_key for obj in objects]).values())

        self.assertEqual(actual, expected)
