# -*- coding: utf-8 -*-
from django_propeller.enums import NavbarItemTypes

try:
    from django.apps import apps
except ImportError:
    apps = False

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class NavBarLinkItem(object):
    name = None
    url = None
    icon = None

    def __init__(self, name="", url=None):
        self.name = name
        self.url = url
        self.type = NavbarItemTypes.link

    def get_url(self):
        if self.url:
            if not str(self.url).startswith('http'):
                return reverse(self.url)
            return self.url
        return "javascript:void(0);"


class NavBarDropDownDivider(object):
    pass


class NavBarDropDownItem(NavBarLinkItem):
    items = []

    def __init__(self, name="", items=None, url=None):
        super(NavBarDropDownItem, self).__init__(name, url)
        if items:
            self.items = items
            self.type = NavbarItemTypes.dropdown


class NavBar(object):
    """
    NavBar is a class that generates a NavBar
    """
    brandname = ""
    brandurl = None
    items = []
    style_inverse = True
    style_static = True

    def get_brand_url(self):
        if self.brandurl:
            if not str(self.brandurl).startswith('http'):
                return reverse(self.brandurl)
            return self.brandurl
        return "javascript:void(0);"
