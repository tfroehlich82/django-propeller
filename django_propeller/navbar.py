# -*- coding: utf-8 -*-


class NavBarItem(object):
    name = None
    url = None

    def __init__(self, name="", url=None):
        self.name = name
        self.url = url

    def get_url(self):
        # if self.url:
        #     return "{% url '{url}' %}".format(url=self.url)
        return "javascript:void(0);"


class NavBar(object):
    brandname = ""
    items = []
