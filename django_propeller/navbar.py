# -*- coding: utf-8 -*-
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class NavBarItem(object):
    name = None
    url = None
    icon = None

    def __init__(self, name="", url=None):
        self.name = name
        self.url = url

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


class NavBar(object):
    brandname = ""
    items = []
