Template Filters
================

* *Method Calling* - A set of filters are provided for calling a method on an
  object in the template. This is useful for cases where you want to run a
  method from the template itself and act on it rather than in the view. While
  it's best practice to not put this type of logic in the template, there are
  cases where you may want to do so.::

    {% load custom_filters %}
    {% if foo|method:"has_access"|with:user|with:group|call %}

    This will invoke foo.has_access(user, group)
