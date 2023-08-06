==============
Django Toolset
==============

.. image:: https://img.shields.io/pypi/l/django-toolset.svg
   :target: https://raw.githubusercontent.com/codezeus/django-toolset/master/LICENSE

.. image:: https://secure.travis-ci.org/codezeus/django-toolset.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/codezeus/django-toolset

.. image:: https://img.shields.io/pypi/v/django-toolset.svg
    :target: https://pypi.python.org/pypi/django-toolset/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-toolset.svg
    :target: https://pypi.python.org/pypi/django-toolset/
    :alt: Number of PyPI downloads

.. image:: https://coveralls.io/repos/github/codezeus/django-toolset/badge.svg?branch=master
   :target: https://coveralls.io/github/codezeus/django-toolset?branch=master
   :alt: Coverage

Django Toolset is a simple package with a few useful models, views,
templatetags, and other functions that can be used to save time when writing a
Django application.

For specific information about what's included, view the `docs`_.

.. _docs: docs/

Requirements
============

Django Toolset requires Django 1.8 or later.

Getting It
==========

You can get Django Toolset by using pip::

    $ pip install django-toolset

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
