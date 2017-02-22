# -*- coding: utf-8 -*-
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
try:
    from enum import Enum
except ImportError:
    from enum34 import Enum


class NavbarItemTypes(Enum):
    link = 1
    dropdown = 2


class NavBarItem(object):
    name = None
    url = None
    icon = None

    def __init__(self, name="", url=None):
        self.name = name
        self.url = url
        self.type = NavbarItemTypes.link

    def get_url(self):
        if self.url:
            return reverse(self.url)
        return "javascript:void(0);"


class NavBarDropDownItem(NavBarItem):
    items = []

    def __init__(self, name="", items=None, url=None):
        super(NavBarDropDownItem, self).__init__(name, url)
        if items:
            self.items = items
            self.type = NavbarItemTypes.dropdown


class NavBar(object):
    brandname = ""
    items = []
    style_inverse = True
