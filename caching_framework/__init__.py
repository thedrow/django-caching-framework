import django.db.models.signals
from caching_framework.queryset import CachingQuerySetMixin


def register(model):
    django.db.models.signals.post_save.connect(lambda sender, instance, **kwargs: instance.cache(),
                                               sender=model,
                                               weak=False,
                                               dispatch_uid='%s_cache_object' % model._meta.db_table)

    django.db.models.signals.pre_delete.connect(lambda sender, instance, **kwargs: instance.uncache(),
                                                sender=model,
                                                weak=False,
                                                dispatch_uid='%s_uncache_object' % model._meta.db_table)
