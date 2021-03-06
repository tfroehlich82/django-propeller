========
Settings
========

The django-propeller has some pre-configured settings.

They can be modified by adding a dict variable called ``PROPELLER`` in your ``settings.py`` and customizing the values ​​you want;

The ``PROPELLER`` dict variable contains these settings and defaults:


.. code:: django

    # Default settings
    PROPELLER = {

        # The URL to the jQuery JavaScript file
        'jquery_url': '//code.jquery.com/jquery.min.js',

        # The Bootstrap base URL
        'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/',

        # The complete URL to the Bootstrap CSS file (None means derive it from base_url)
        'css_url': None,

        # The complete URL to the Bootstrap CSS file (None means no theme)
        'theme_url': None,

        # The complete URL to the Bootstrap JavaScript file (None means derive it from base_url)
        'javascript_url': None,

        # Put JavaScript in the HEAD section of the HTML document (only relevant if you use propeller.html)
        'javascript_in_head': False,

        # Include jQuery with Bootstrap JavaScript (affects django-propeller template tags)
        'include_jquery': False,

        # Label class to use in horizontal forms
        'horizontal_label_class': 'col-md-3',

        # Field class to use in horizontal forms
        'horizontal_field_class': 'col-md-9',

        # Set HTML required attribute on required fields, for Django <= 1.8 only
        'set_required': True,

        # Set HTML disabled attribute on disabled fields, for Django <= 1.8 only
        'set_disabled': False,

        # Set placeholder attributes to label if no placeholder is provided
        'set_placeholder': True,

        # Class to indicate required (better to set this in your Django form)
        'required_css_class': '',

        # Class to indicate error (better to set this in your Django form)
        'error_css_class': 'has-error',

        # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
        'success_css_class': 'has-success',

        # Renderers (only set these if you have studied the source and understand the inner workings)
        'formset_renderers':{
            'default': 'propeller.renderers.FormsetRenderer',
        },
        'form_renderers': {
            'default': 'propeller.renderers.FormRenderer',
        },
        'field_renderers': {
            'default': 'propeller.renderers.FieldRenderer',
            'inline': 'propeller.renderers.InlineFieldRenderer',
        },
    }
