========
Overview
========

Architecture
============

Django Caching Framework caches items and invalidates them asynchronously using Celery.
Celery stores the items in the cache after they are fetched from the database.

Cache Buckets
-------------

Objects Cache Bucket
````````````````````

The objects cache bucket stores single objects by their primary key and by their unique fields.
For example the following model:

.. code-block:: python

    from django.db import models
    from django.contrib.auth.models import User
    from django.utils.text import slugify

    class Post(models.Model):
        title = models.CharField(max_length=256, unique_for_date='created_at')
        created_at = models.DateTimeField(auto_now_add=True)
        slug = models.SlugField(unique=True)
        author = models.ForeignKey(to=User)

        def save(self, *args, *kwargs):
            if not self.slug:
                self.slug = slugify(self.title + str(self.created_at))
            super(Post, self).save(*args, **kwargs)

        class Meta:
            app_label = 'blog'
            unique_with = ('title', 'author')

Would generate the following cache keys:
* blog_post:pk=<pk>
* blog_post:slug=<slug>
* blog_post:author=<author>;title=<title>;created_at=<created_at>
* blog_post:title=<title>;created_at=<created_at>
* blog_post:pk=<pk>;slug=<slug>
* blog_post:pk=<pk>;author=<author>;title=<title>;created_at=<created_at>
* blog_post:pk=<pk>;title=<title>;created_at=<created_at>

For each object that was created.

So the following queries would be fetched from the cache:

.. doctest::

    >>> Post.objects.create(pk=1, slug='new-post', title="new post", author_id=1) # Caches the object
    <Post: Post object>
    >>> Post.objects.get(pk=1) == objects_cache.get('blog_post:pk=1')
    True
    >>> Post.objects.filter(slug='new-post').exists() == True # If the key blog_post:slug=new-post exists then the object exists.
    True
    >>> Post.objects.get_or_create(title="new post", author_id=1) == objects_cache.get('blog_post:author_id=1;title=new post')
    True

Queries Cache Bucket
````````````````````

The queries cache bucket stores query results and objects by their indexes.
Let's take the Post model from the example above and add indexes:

.. code-block:: python

    from django.db import models
    from django.contrib.auth.models import User
    from django.utils.text import slugify

    class Post(models.Model):
        title = models.CharField(max_length=256, unique_for_date='created_at')
        created_at = models.DateTimeField(auto_now_add=True, db_index=True)
        slug = models.SlugField(unique=True)
        author = models.ForeignKey(to=User)

        def save(self, *args, *kwargs):
            if not self.slug:
                self.slug = slugify(self.title + str(self.created_at))
            super(Post, self).save(*args, **kwargs)

        class Meta:
            app_label = 'blog'
            unique_with = ('title', 'author')
            index_with = ('title', 'author', 'created_at')

Would generate the following cache keys:
* blog_post:queries:created_at=<created_at>
* blog_post:queries:title=<title>;author=<author>

So the following queries would be fetched from the cache:

.. doctest::

    >>> Post.objects.create(pk=1, slug='new-post', title="new post", author_id=1) # Caches the object
    <Post: Post object>
    >>> Post.objects.order_by('title', 'author')
    [<Post: Post object>]
    >>> Post.objects.order_by('-title', 'author') # The query results will be fetched from the cache if the backend supports sorting
    [<Post: Post object>]
    >>> Post.objects.filter(title="new post", author_id=1, created_at=datetime.now()) # The query results will be fetched from the cache if the backend supports filtering
    [<Post: Post object>]

Pages Cache Bucket
``````````````````

Stores view responses.

Most Recently Used Bucket
`````````````````````````

Stores the most used items in a cache backend that is in memory in order to save network I/O overhead.