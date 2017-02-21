# -*- coding: utf-8 -*-


class NavBarItem(object):

    def __init__(self, name="", url="javascript:void(0);"):
        self.name = name
        self.url = url


class NavBar(object):

    def __init__(self, brand, items=None):
        if items is None:
            items = []
        self.brandname = brand
        self.items = items
