import django

if django.VERSION >= (1, 7):  # pragma: nocover
    from django.core.cache import caches

    def get_cache(name):
        return caches[name]
else:
    from django.core.cache import get_cache  # pragma: nocover

