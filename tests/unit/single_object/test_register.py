from unittest import TestCase

import caching_framework
from caching_framework.queryset import CachingQuerySetMixin
from tests.compat import mock
from tests.unit.support.models import TestModel


class RegisterTestCase(TestCase):
    def test_post_save_hook_was_connected(self):
        with mock.patch('django.db.models.signals.post_save') as mocked_post_save, \
                mock.patch('django.db.models.signals.pre_delete'):
            caching_framework.register(TestModel)

            mocked_post_save.connect.assert_called_once_with(mock.ANY,
                                                             sender=TestModel,
                                                             weak=False,
                                                             dispatch_uid='%s_cache_object' % TestModel._meta.db_table)

    def test_pre_delete_hook_was_connected(self):
        with mock.patch('django.db.models.signals.post_save'), \
                mock.patch('django.db.models.signals.pre_delete') as mocked_pre_delete:
            caching_framework.register(TestModel)

            mocked_pre_delete.connect.assert_called_once_with(mock.ANY,
                                                              sender=TestModel,
                                                              weak=False,
                                                              dispatch_uid='%s_uncache_object' % TestModel._meta.db_table)
