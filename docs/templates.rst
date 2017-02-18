=========
Templates
=========

You can customize the output of ``django-propeller`` by writing your own templates. These templates are available:


propeller/field_help_text_and_errors.html
-----------------------------------------

This renders the help text and error of each field.

Variable ``help_text_and_errors`` contains an array of strings.


propeller/form_errors.html
--------------------------

This renders the non field errors of a form.

Variable ``errors`` contains an array of strings.


propeller/messages.html
-----------------------

This renders the Django messages variable.

Variable ``messages`` contains the messages as described in https://docs.djangoproject.com/en/dev/ref/contrib/messages/#displaying-messages

``messages`` is passed through three built-in filters

`safe <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-safe>`

`urlize <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-urlize>`

`linebreaksbr <https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatefilter-linebreaksbr>`

Other
-----

There are two more templates, ``propeller/propeller.html`` and ``propeller/pagination.html``. You should consider these private for now, meaning you can use them but not modify them.
