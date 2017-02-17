Propeller for Django
====================

Write Django as usual, and let ``django-propeller`` make template output into code based on Google's Material Design Standards & Bootstrap.


![Travis CI](http://img.shields.io/travis/joyent/django-propeller.svg)
![PyPI version](http://img.shields.io/pypi/v/django-propeller.svg)
![PyPI downloads](http://img.shields.io/pypi/dm/django-propeller.svg)


Requirements
------------

- Python 2.7, 3.2, 3.3, 3.4, or 3.5
- Django >= 1.10


Installation
------------

1. Install using pip:
```
    pip install django-propeller
```

2. Add to INSTALLED_APPS in your ``settings.py``:

   ```
   'django_propeller',
   ```

3. In your templates, load the ``django_propeller`` library and use the ``propeller_*`` tags:



Example template
----------------

```
    {% load bootstrap3 %}

    {# Display a form #}

    <form action="/url/to/submit/" method="post" class="form">
        {% csrf_token %}
        {% bootstrap_form form %}
        {% buttons %}
            <button type="submit" class="btn btn-primary">
                {% bootstrap_icon "star" %} Submit
            </button>
        {% endbuttons %}
    </form>
```


Documentation
-------------

The full documentation is at http://django-propeller.readthedocs.io/.


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/tfroehlich82/django-propeller/issues


License
-------

You can use this under MIT License. See [LICENSE](LICENSE) file for details.


Author
------

Developed and maintained by [Thorsten Fröhlich](https://github.com/tfroehlich82),
based on the idea of django-bootstrap3 from [Dylan Verheul](https://github.com/dyve).
