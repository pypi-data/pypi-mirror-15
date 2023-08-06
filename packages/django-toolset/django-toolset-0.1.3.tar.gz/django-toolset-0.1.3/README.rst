==============
Django Toolset
==============

Django Toolset is a simple package with a few useful models, views,
templatetags, and other functions that can be used to save time when writing a
Django application.

Requirements
============

Django Toolset requires Django 1.8 or later.

Getting It
==========

You can get Django Toolset by using pip or easy_install::

    $ pip install django-toolset
    or
    $ easy_install django-toolset

If you want to install it from source, grab the git repository from GitHub and run setup.py::

    $ git clone git://github.com/codezeus/django-toolset.git
    $ cd django-toolset
    $ python setup.py install

Installing It
=============

To enable `django_toolset` in your project you need to add it to `INSTALLED_APPS` in your projects
`settings.py` file::

    INSTALLED_APPS = (
        ...
        'django_toolset',
        ...
    )

Getting Involved
================

Open Source projects can always use more help. Fixing a problem, documenting a
feature, and adding translations in your language. If you have some time to spare
and like to help us, please submit a pull request.
