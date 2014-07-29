============
Installation
============

Using pip
=========

At the command line::

    $ pip install django-caching-framework

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv <virtualenv name> -i django-caching-framework

From Source
===========

In order to install from source simply type::

    $ git clone http//github.com/thedrow/django-caching-framework.git
    $ cd django-caching-framework
    $ mkvirtualenv django-caching-framework
    $ python setup.py install

Installing the cache backends
=============================
* Memcached::

    $ pip install django-caching-framework[memcached]
* Redis::

    $ pip install django-caching-framework[redis]
* uWSGI::

    $ pip install django-caching-framework[uWSGI]

Make sure you select the `correct build profile`_ (or use the default).

Installing Celery
=================

Celery is installed by default with RabbitMQ support.
If you would like to use a different broker please follow Celery's `documentation`_.

.. _correct build profile: http://uwsgi-docs.readthedocs.org/en/latest/Install.html?highlight=uwsgi_profile#alternative-build-profiles
.. _documentation: https://celery.readthedocs.org/en/latest/getting-started/brokers/index.html