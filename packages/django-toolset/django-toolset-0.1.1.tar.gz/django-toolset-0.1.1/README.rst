==============
Django-Toolset
==============

Django-Toolset is a simple package with a few useful models, views,
templatetags, and other functions that can be used to save time when writing a
Django application.

Detailed documentation is in the "docs" directory.

Quick Start
-----------

1. Add "django_toolset" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
       ...
       'djangp_toolset',
   ]

2. If you choose to use the `authenticated_redirect` decorator, specify the
   `DEFAULT_AUTHENTICATED_PATH` in your settings file (it defaults to
   "dashboard")
