========================
Django Caching Framework
========================

Django Caching Framework is a toolbox that allows you to asynchronously cache objects, queries and pages.
It supports event driven invalidation, cache warmup and provides multiple strategies for storing and fetching items
from the cache.

Supported Python Versions
=========================

* Python 2.7+
* Python 3.3+
* PyPy 2.3+

Requirements
============

* Django>=1.6
* Celery>=3.1

Cache Backends
==============

* Memcached
* Redis
* uWSGI

Cache Buckets
=============

* Objects Cache
* Queries Cache
* Pages Cache
* Most Recently Used Cache