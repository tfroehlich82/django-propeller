# -*- coding: utf-8 -*-
from .components import Button, FAB


class CardTitle(object):
    text = ""
    size = 3

    def as_html(self):
        return '<h%d class ="pmd-card-title-text">%s</h%d>' % (self.size, self.text, self.size)


class CardSubtitle(object):
    text = ""

    def as_html(self):
        return '<span class="pmd-card-subtitle-text">%s</span>' % self.text


class CardHeader(object):
    content_left = []
    content_middle = []

    def as_html(self):
        tag = '<div class="pmd-card-title">'
        tag += '<div class ="media-left">'
        for itm in self.content_left:
            tag += itm.as_html()
        tag += '</div><div class ="media-body media-middle">'
        for itm in self.content_middle:
            tag += itm.as_html()
        tag += '</div></div>'
        return tag


class CardMediaActions(object):
    items = []

    def as_html(self):
        tag = '<div class="pmd-card-actions">'
        for btn in self.items:
            if isinstance(btn, FAB):
                tag += btn.as_html()
        tag += '</div>'
        return tag


class CardActions(object):
    items = []

    def as_html(self):
        tag = '<div class="pmd-card-actions">'
        for btn in self.items:
            if isinstance(btn, Button):
                tag += btn.as_html()
        tag += '</div>'
        return tag


class CardMedia(object):
    orientation = 'default'
    content = None


class Card(object):
    """Card is a class that generates a Propeller Card"""
    primary_title = None
    secondary_title = None
    header = None
    media = None
    body = None
    actions = None
    media_actions = None
    style_inverse = False
    style_inline = False
    width = 4
