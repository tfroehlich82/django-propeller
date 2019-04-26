# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django import VERSION as DJANGO_VERSION
from django.conf import settings

# Do we support set_required and set_disabled?
# See GitHub issues 337 and 345
# TODO: Get rid of this after support for Django 1.8 LTS ends
PROPELLER_SET_REQUIRED_SET_DISABLED = DJANGO_VERSION[0] < 2 and DJANGO_VERSION[1] < 10

# Default settings
PROPELLER_DEFAULTS = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',

    'set_placeholder': True,
    'required_css_class': '',
    'error_css_class': 'has-error',
    'success_css_class': 'has-success',
    'formset_renderers': {
        'default': 'django_propeller.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'django_propeller.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'django_propeller.renderers.FieldRenderer',
        'inline': 'django_propeller.renderers.InlineFieldRenderer',
    },
}

if PROPELLER_SET_REQUIRED_SET_DISABLED:
    PROPELLER_DEFAULTS.update({
        'set_required': True,
        'set_disabled': False,
    })

# Start with a copy of default settings
PROPELLER = PROPELLER_DEFAULTS.copy()

# Override with user settings from settings.py
PROPELLER.update(getattr(settings, 'PROPELLER', {}))


def get_propeller_setting(setting, default=None):
    """
    Read a setting
    """
    return PROPELLER.get(setting, default)


def propeller_url(postfix):
    """
    Prefix a relative url with the Propeller base url
    """
    return get_propeller_setting('base_url') + postfix


def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return get_propeller_setting('jquery_url')


def javascript_url():
    """
    Return the full url to the Propeller JavaScript file
    """
    return get_propeller_setting('javascript_url') or propeller_url('js/bootstrap.min.js')


def css_url():
    """
    Return the full url to the Propeller CSS file
    """
    return get_propeller_setting('css_url') or propeller_url('css/bootstrap.min.css')


def theme_url():
    """
    Return the full url to the theme CSS file
    """
    return get_propeller_setting('theme_url')


def get_renderer(renderers, **kwargs):
    layout = kwargs.get('layout', '')
    path = renderers.get(layout, renderers['default'])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_propeller_setting('formset_renderers')
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_propeller_setting('form_renderers')
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_propeller_setting('field_renderers')
    return get_renderer(renderers, **kwargs)
