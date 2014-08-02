from django.db.models import Model, Manager, CharField, IntegerField, DateTimeField

import caching_framework
from caching_framework.mixins import CachingMixin
from caching_framework.queryset import CachingQuerySet


class TestManager(Manager):
    def get_queryset(self):
        return CachingQuerySet(model=self.model)


class TestModel(CachingMixin, Model):
    foo = CharField(max_length=20, null=True, unique=True)
    bar = IntegerField(null=True, unique_for_date='created_at')
    created_at = DateTimeField(auto_now_add=True)

    objects = TestManager()

    def __str__(self):
        return 'PK=%s;foo=%s;bar=%s' % (self.pk, self.foo, self.bar)

    def __eq__(self, other):
        return self.pk == other.pk and self.foo == other.foo and self.bar == other.bar

    class Meta:
        unique_together = ('foo', 'bar')


caching_framework.register(TestModel)
