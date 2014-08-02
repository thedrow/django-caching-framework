from datetime import datetime
from unittest import TestCase
from caching_framework.keys import CacheKeysGenerator
from tests.unit.support.models import TestModel


class ObjectsCacheKeysGeneratorTestCase(TestCase):
    def test_foo_cache_key_is_generated(self):
        model = TestModel(foo='test', bar=1)
        sut = CacheKeysGenerator(model)
        expected = '%s:foo=test' % model._meta.db_table

        actual = tuple(sut.object_cache_keys)

        self.assertIn(expected, actual, "%s not found in:\n %s" % (expected, '\n or in '.join(actual)))

    def test_foo_and_bar_cache_key_is_generated(self):
        model = TestModel(foo='test', bar=1)
        sut = CacheKeysGenerator(model)
        expected = '%s:foo=test;bar=1' % model._meta.db_table

        actual = tuple(sut.object_cache_keys)

        self.assertIn(expected, actual, "%s not found in:\n %s" % (expected, '\n or in '.join(actual)))

    def test_bar_and_created_at_cache_key_is_generated(self):
        model = TestModel(foo='test', bar=1, created_at=datetime.now())
        sut = CacheKeysGenerator(model)
        expected = '%s:bar=1;created_at=%s' % (model._meta.db_table, model.created_at)

        actual = tuple(sut.object_cache_keys)

        self.assertIn(expected, actual, "%s not found in:\n %s" % (expected, '\n or in '.join(actual)))

    def test_pk_cache_key_is_generated(self):
        model = TestModel(pk=1, foo='test', bar=1)
        sut = CacheKeysGenerator(model)
        expected = '%s:pk=1' % model._meta.db_table

        actual = tuple(sut.object_cache_keys)

        self.assertIn(expected, actual, "%s not found in:\n %s" % (expected, '\n or in '.join(actual)))
