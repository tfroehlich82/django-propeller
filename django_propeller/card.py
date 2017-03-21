# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

from .utils import render_tag
from .components import Button, FAB, Image
from .text import text_concat


class CardTitle(object):
    text = ""
    size = 3

    def as_html(self):
        tag = 'h%d' % self.size
        attrs = {'class': 'pmd-card-title-text'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardSubtitle(object):
    text = ""

    def as_html(self):
        tag = 'span'
        attrs = {'class': 'pmd-card-subtitle-text'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardBody(object):
    text = ""

    def as_html(self):
        tag = 'div'
        attrs = {'class': 'pmd-card-body'}
        content = self.text
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardHeader(object):
    content_left = []
    content_middle = []

    def get_left_content(self):
        tag = 'div'
        attrs = {'class': 'media-left'}
        content = ''
        for itm in self.content_left:
            content = text_concat(content, mark_safe(itm.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def get_middle_content(self):
        tag = 'div'
        attrs = {'class': 'media-body media-middle'}
        content = ''
        for itm in self.content_middle:
            content = text_concat(content, mark_safe(itm.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )

    def as_html(self):
        tag = 'div'
        attrs = {'class': 'pmd-card-title'}
        content = text_concat(self.get_left_content(), self.get_middle_content())
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardMediaActions(object):
    items = []

    def as_html(self):
        tag = 'div'
        attrs = {'class': 'pmd-card-actions'}
        content = ''
        for btn in self.items:
            if isinstance(btn, FAB):
                content = text_concat(content, mark_safe(btn.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardActions(object):
    items = []

    def as_html(self):
        tag = 'div'
        attrs = {'class': 'pmd-card-actions'}
        content = ''
        for btn in self.items:
            if isinstance(btn, Button):
                content = text_concat(content, mark_safe(btn.as_html()))
        return render_tag(tag, attrs=attrs, content=mark_safe(content), )


class CardMedia(object):
    orientation = 'default'
    content = None

    def as_html(self):
        if isinstance(self.content, Image):
            return self.content.as_html()


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
