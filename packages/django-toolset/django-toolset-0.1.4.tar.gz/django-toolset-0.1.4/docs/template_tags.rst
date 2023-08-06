Template Tags
=============

* *active* - The active template tag is an easy way to output a class name for
  the currently active link. This is useful if you're creating a navigation
  component and want to give the active URL a specific class for UI purposes.
  It will accept a named URL or a regex pattern.::

    {% load custom_tags %}
    <nav>
      <ul>
        <li class="nav-home {% active 'url-name' %}"><a href="#">Home</a></li>
        <li class="nav-blog {% active '^/regex/' %}"><a href="#">Blog</a></li>
      </ul>
    </nav>

    or

    <nav>
      <ul>
        <li class="nav-home {% active 'url-name' class_name='current' %}"><a href="#">Home</a></li>
        <li class="nav-blog {% active '^/regex/' class_name='current' %}"><a href="#">Blog</a></li>
      </ul>
    </nav>
