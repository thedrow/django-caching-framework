from django.db.models import Model, Manager, CharField, IntegerField

import caching_framework
from caching_framework.mixins import CachingMixin
from caching_framework.queryset import CachingQuerySet


class TestManager(Manager):
    def get_queryset(self):
        return CachingQuerySet(model=self.model)


class TestModel(CachingMixin, Model):
    objects = TestManager()
    foo = CharField(max_length=20, null=True)
    bar = IntegerField(null=True)

    def __str__(self):
        return 'PK=%d;foo=%s;bar=%s' % (self.pk, self.foo, self.bar)

    def __eq__(self, other):
        return self.pk == other.pk and self.foo == other.foo and self.bar == other.bar


caching_framework.register(TestModel)
