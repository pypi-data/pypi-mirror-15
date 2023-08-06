Decorators
==========

* *authenticated_redirect* - authenticated_redirect provides a way to redirect
  a user from pages they shouldn't visit when they have been authenticated.
  For instance, if a user is logged in then they shouldn't visit the "login"
  page. By default, this will redirect users to a URL named "dashboard" but
  this can be overwritten with the settings variable
  `DEFAULT_AUTHENTICATED_PATH`. If you wish to set the path explicitly for
  each view you can do so by passing the `path` kwarg to the decorator::

    settings.py

    DEFAULT_AUTHENTICATED_PATH = 'admin'

    views.py

    @authenticated_redirect
    def my_view(request):
        """This redirects to `admin` if logged in"""
        ...

    @authenticated_redirect(path='some_other_page')
    def my_other_view(request):
        """This redirects to `some_other_page` if logged in"""
        ...
