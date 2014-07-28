def generate_cache_key(obj):
    if obj.pk is None:
        raise ValueError("Cannot generate a cache key for an unsaved object")

    return '%s:%s' % (obj._meta.db_table, obj.pk)
