# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from collections import Mapping

try:  # pragma: no cover
    from urllib.parse import urlencode
except ImportError:  # pragma: no cover
    from urllib import urlencode

try:  # pragma: no cover
    from urllib.parse import urlparse, parse_qs, urlunparse
except ImportError:  # pragma: no cover
    from urlparse import urlparse, parse_qs, urlunparse

from django.forms.utils import flatatt
from django.template.loader import get_template
from django.utils.encoding import force_str, force_text
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from .text import text_value

# RegEx for quoted string
QUOTED_STRING = re.compile(r'^["\'](?P<noquotes>.+)["\']$')


def split_css_classes(css_classes):
    """Turn string into a list of CSS classes"""
    classes_list = text_value(css_classes).split(' ')
    return [c for c in classes_list if c]


def add_css_class(css_classes, css_class, prepend=False):
    """Add a CSS class to a string of CSS classes"""
    classes_list = split_css_classes(css_classes)
    classes_to_add = [c for c in split_css_classes(css_class)
                      if c not in classes_list]
    if prepend:
        classes_list = classes_to_add + classes_list
    else:
        classes_list += classes_to_add
    return ' '.join(classes_list)


def render_link_tag(url, rel='stylesheet', media=None):
    """Build a link tag"""
    attrs = {
        'href': url,
        'rel': rel,
    }
    if media:
        attrs['media'] = media
    return render_tag('link', attrs=attrs, close=False)


def render_tag(tag, attrs=None, content=None, close=True):
    """Render a HTML tag"""
    builder = '<{tag}{attrs}>{content}'
    if content or close:
        builder += '</{tag}>'
    return format_html(
        builder,
        tag=tag,
        attrs=mark_safe(flatatt(attrs)) if attrs else '',
        content=text_value(content),
    )


def render_template_file(template, context=None):
    """Render a Template to unicode"""
    assert isinstance(context, Mapping)
    template = get_template(template)
    return template.render(context)


def url_replace_param(url, name, value):
    """Replace a GET parameter in an URL"""
    url_components = urlparse(force_str(url))
    query_params = parse_qs(url_components.query)
    query_params[name] = value
    query = urlencode(query_params, doseq=True)
    return force_text(urlunparse([
        url_components.scheme,
        url_components.netloc,
        url_components.path,
        url_components.params,
        query,
        url_components.fragment,
    ]))
