# -*- coding: utf-8 -*-

"""This module contains classes for constructing propeller navbars"""

from django.utils.safestring import mark_safe

from .utils import render_tag, add_css_class
from .text import text_concat

try:  # pragma: no cover
    from django.urls import reverse
except ImportError:  # pragma: no cover
    from django.core.urlresolvers import reverse


class NavBarLinkItem(object):

    """
    Generates a Link navbar item or a Link DropDown item.

    **Parameters**:

        name
            The display name for the item. (for example: 'Home')

        url
            The address for the link item. Can be a absolute URL or a resolvable Django url.
            (for example: 'http://example.org' or 'home'). Optional.

        icon
            not yet supported
    """

    name = None
    url = None
    icon = None

    def __init__(self, name="", url=None, icon=None):
        """

         
        """
        self.name = name
        self.url = url
        self.icon = icon

    def get_url(self):
        """
        Returns the url set in the attribute.

        **Returns**

            ``javascript:void(0);`` if ``url = None``

            or

            an absolute URL if ``url`` starts with 'http'

            or

            an relative URL if ``url`` is a resolvable Django url
        """
        if self.url:
            if not str(self.url).startswith('http'):
                return reverse(self.url)
            return self.url
        return "javascript:void(0);"

    def as_html(self):
        """Returns navbar link item as html"""
        tag = 'a'
        attrs = {'class': 'pmd-ripple-effect', 'href': self.get_url()}
        content = self.name
        return '<li>' + render_tag(tag, attrs=attrs, content=mark_safe(content), ) + '</li>'


class NavBarDropDownDivider(object):

    """Generates a DropDown Divider item."""

    @staticmethod
    def as_html():
        """Returns navbar dropdown divider as html"""
        tag = 'li'
        attrs = {'role': 'separator', 'class': 'divider'}
        return render_tag(tag, attrs=attrs, )


class NavBarDropDownItem(NavBarLinkItem):

    """
    Generates a DropDown navbar item.

    **Parameters**:

        name
            The display name for the item. (for example: 'Home')

        url
            The address for the link item. Can be a absolute URL or a resolvable Django url.
            (for example: 'http://example.org' or 'home'). Optional.

        icon
            not yet supported

        items
            A list containing NavBarLinkItems and/or NavBarDropDownDivider. Optional.
    """

    items = []

    def __init__(self, name="", items=None, url=None):
        super(NavBarDropDownItem, self).__init__(name, url)
        if items:
            self.items = items

    def as_html(self):
        """Returns navbar dropdown item as html"""
        tag = 'li'
        attrs = {'class': 'dropdown pmd-dropdown'}
        content = '<a data-toggle="dropdown" class="pmd-ripple-effect dropdown-toggle" data-sidebar="true" ' \
                  'href="%s">%s<span class="caret"></span></a>' % (self.url, self.name)
        content = text_concat(content, '<ul class="dropdown-menu">')
        for itm in self.items:
            content = text_concat(content, itm.as_html())
        content = text_concat(content, '</ul>')

        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class NavBar(object):

    """
    NavBar is a class that generates a NavBar.

    **Parameters**:

        brandname
            The brand shown on the very left of the navbar.

        brandurl
            The address for the brand name. Can be a absolute URL or a resolvable Django url.
            (for example: 'http://example.org' or 'home'). Optional.

        items
            A list containing NavBarLinkItems and/or NavBarDropDownItems. Optional.

        style_inverse
            Generate a dark navbar if true (default) or a light navbar if false.

        style_static
            Sets the static style for the navbar. Static if true (default) or floating on top if false.
    """

    brandname = ""
    brandurl = None
    items = []
    style_inverse = True
    style_static = True

    def get_brand_url(self):
        """
        Returns the brand url set in the attribute.

        **Returns**

            ``javascript:void(0);`` if ``brandurl = None``

            or

            an absolute URL if ``brandurl`` starts with 'http'

            or

            an relative URL if ``brandurl`` is a resolvable Django url
        """
        if self.brandurl:
            if not str(self.brandurl).startswith('http'):
                return reverse(self.brandurl)
            return self.brandurl
        return "javascript:void(0);"

    @staticmethod
    def render_toggle():
        """Returns navbar toggle as html (for responsive)"""
        tag = 'button'
        attrs = {
            'class': 'navbar-toggle collapsed',
            'type': 'button',
            'data-toggle': 'collapse',
            'aria-expanded': 'false'
        }
        content = '<span class="sr-only">Toggle navigation</span>'
        content = text_concat(content, '<span class="icon-bar"></span>')
        content = text_concat(content, '<span class="icon-bar"></span>')
        content = text_concat(content, '<span class="icon-bar"></span>')
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def render_header(self):
        """Returns navbar header as html"""
        tag = 'div'
        attrs = {'class': 'navbar-header'}
        content = self.render_toggle()
        content = text_concat(content, '<a href="%s" class="navbar-brand navbar-brand-custome">%s'
                                       '</a>' % (self.get_brand_url(), self.brandname))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def render_items(self):
        """Returns navbar items as html (for item container)"""
        tag = 'ul'
        attrs = {'class': 'nav navbar-nav'}
        content = ''
        for itm in self.items:
            content = text_concat(content, itm.as_html())
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def render_item_container(self):
        """Returns navbar items as html"""
        tag = 'div'
        attrs = {'class': 'collapse navbar-collapse'}
        content = self.render_items()
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def render_content(self):
        """Returns navbar content as html"""
        tag = 'div'
        attrs = {'class': 'container-fluid'}
        content = self.render_header()
        content = text_concat(content, self.render_item_container())
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def as_html(self):
        """Returns navbar as html"""
        tag = 'nav'
        classes = 'navbar'
        if self.style_inverse:
            classes = add_css_class(classes, 'navbar-inverse')
        if self.style_static:
            classes = add_css_class(classes, 'navbar-static')
        else:
            classes = add_css_class(classes, 'navbar-top')
        classes = add_css_class(classes, 'pmd-navbar')
        classes = add_css_class(classes, 'pmd-z-depth')
        attrs = {'class': classes}
        content = self.render_content()
        content = text_concat(content, '<div class="pmd-sidebar-overlay"></div>')
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )
