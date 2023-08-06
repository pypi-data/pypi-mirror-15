Introduction
============

django-fs-leonid is the Django-related reusable app provides the ability to create and store in a database files such as robots.txt, sitemap.xml and so on.


Installation
============

1. Install ``django-fs-leonid`` using ``pip``::

    $ pip install django-fs-leonid

2. Add ``'leonid'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'leonid',
        ...
    )

3. Update your ``urls.py``::

    url(r'^', include('leonid.urls')),

4. Run ``syncdb`` or ``migrate``::

    $ ./manage.py syncdb

    or

    $ ./manage.py migrate


Credits
=======

`Fogstream <http://fogstream.ru>`_
