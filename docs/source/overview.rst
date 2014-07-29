========
Overview
========

Architecture
============

Django Caching Framework caches items and invalidates them asynchronously using Celery.
Celery stores the objects in the cache after they are fetched from the database.

Cache Buckets
-------------

Objects Cache Bucket
````````````````````

Stores single objects by their primary key and optionally by their unique fields.

Queries Cache Bucket
````````````````````

Stores query results.

Pages Cache Bucket
``````````````````

Stores view responses.

Most Recently Used Bucket
`````````````````````````

Stores the most used items in a cache backend that is in memory in order to save network I/O overhead.