# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.safestring import mark_safe

from django_propeller.exceptions import PropellerError
from django_propeller.utils import render_tag, add_css_class

from .text import text_value, text_concat


def render_icon(icon, size='sm', **kwargs):
    """
    Render a Google icon
    """
    attrs = {
        'class': add_css_class(
            'material-icons md-dark pmd-{size}'.format(size=size),
            kwargs.get('extra_classes', ''),
        )
    }
    title = kwargs.get('title')
    if title:
        attrs['title'] = title
    return render_tag('i', attrs=attrs, content=icon)


def render_bootstrap_icon(icon, **kwargs):
    """
    Render a Bootstrap glyphicon icon
    """
    attrs = {
        'class': add_css_class(
            'glyphicon glyphicon-{icon}'.format(icon=icon),
            kwargs.get('extra_classes', ''),
        )
    }
    title = kwargs.get('title')
    if title:
        attrs['title'] = title
    return render_tag('span', attrs=attrs)


def render_alert(content, alert_type=None, dismissable=True):
    """
    Render a Bootstrap alert
    """
    button = ''
    if not alert_type:
        alert_type = 'info'
    css_classes = ['alert', 'alert-' + text_value(alert_type)]
    if dismissable:
        css_classes.append('alert-dismissable')
        button = '<button type="button" class="close" ' + \
                 'data-dismiss="alert" aria-hidden="true">&times;</button>'
    button_placeholder = '__BUTTON__'
    return mark_safe(render_tag(
        'div',
        attrs={'class': ' '.join(css_classes)},
        content=button_placeholder + text_value(content),
    ).replace(button_placeholder, button))


class Image(object):
    source = ""
    link = None
    width = None
    height = None
    responsive = False
    avatar = False

    def __init__(self, source="", link=None, width=None, height=None, responsive=False, avatar=False):
        self.source = source
        self.link = link
        self.width = width
        self.height = height
        self.responsive = responsive
        self.avatar = avatar

    def as_html(self):
        img_str = ''
        if self.link:
            img_str += '<a'
            if self.avatar:
                img_str += ' class="avatar-list-img"'
            img_str += '>'
        img_str += '<img src="%s"' % self.source
        if self.width:
            img_str += ' width="%d"' % int(self.width)
        if self.height:
            img_str += ' height="%d"' % int(self.height)
        if self.responsive:
            img_str += ' class="img-responsive"'
        img_str += '>'
        if self.link:
            img_str += '</a>'
        return img_str


class Button(object):  # ToDo
    attrs = {}
    content = ""

    def __init__(self, content, button_type=None, icon=None, button_class='btn-default', size='',
                 href='', name=None, value=None, title=None, style='default', extra_classes='', _id=''):
        """
        Render a button with content
        """
        pmd_class = 'pmd-ripple-effect'
        classes = add_css_class('btn', button_class)
        classes = add_css_class(classes, pmd_class)
        size = text_value(size).lower().strip()
        self.content = content
        if size == 'xs':
            classes = add_css_class(classes, 'btn-xs')
        elif size == 'sm' or size == 'small':
            classes = add_css_class(classes, 'btn-sm')
        elif size == 'lg' or size == 'large':
            classes = add_css_class(classes, 'btn-lg')
        elif size == 'md' or size == 'medium':
            pass
        elif size:
            raise PropellerError(
                'Parameter "size" should be "xs", "sm", "lg" or ' +
                'empty ("{}" given).'.format(size))
        if button_type:
            if button_type not in ('submit', 'reset', 'button', 'link'):
                raise PropellerError(
                    'Parameter "button_type" should be "submit", "reset", ' +
                    '"button", "link" or empty  ("{}" given).'.format(button_type))
            self.attrs['type'] = button_type
        if style not in ('default', 'raised', 'flat', 'outline'):
            raise PropellerError(
                'Parameter "style" should be "default", "raised", ' +
                '"flat", "outline" or empty  ("{}" given).'.format(style))
        else:
            classes = add_css_class(classes, 'pmd-btn-%s' % style)
        classes = add_css_class(classes, extra_classes)
        self.attrs['class'] = classes
        self.icon_content = render_icon(icon) if icon else ''
        if href:
            self.attrs['href'] = href
            self.tag = 'a'
        else:
            self.tag = 'button'
        if _id:
            self.attrs['id'] = _id
        if name:
            self.attrs['name'] = name
        if value:
            self.attrs['value'] = value
        if title:
            self.attrs['title'] = title

    def as_html(self):
        return render_tag(self.tag, attrs=self.attrs,
                          content=mark_safe(text_concat(self.icon_content, self.content, separator=' ')), )


class FAB(object):  # ToDo
    attrs = {}
    content = ""

    def __init__(self, content, button_type=None, icon=None, button_class='btn-default', size='', href='',
                 name=None, value=None, title=None, style='default', extra_classes='', _id=''):
        """
        Render a button with content
        """
        pmd_class = 'pmd-btn-fab pmd-ripple-effect'
        classes = add_css_class('btn', button_class)
        classes = add_css_class(classes, pmd_class)
        size = text_value(size).lower().strip()
        self.content = content
        if size == 'xs':
            classes = add_css_class(classes, 'btn-xs')
        elif size == 'sm' or size == 'small':
            classes = add_css_class(classes, 'btn-sm')
        elif size == 'lg' or size == 'large':
            classes = add_css_class(classes, 'btn-lg')
        elif size == 'md' or size == 'medium':
            pass
        elif size:
            raise PropellerError(
                'Parameter "size" should be "xs", "sm", "lg" or ' +
                'empty ("{}" given).'.format(size))
        if button_type:
            if button_type not in ('submit', 'reset', 'button', 'link'):
                raise PropellerError(
                    'Parameter "button_type" should be "submit", "reset", ' +
                    '"button", "link" or empty  ("{}" given).'.format(button_type))
            self.attrs['type'] = button_type
        if style not in ('default', 'raised', 'flat', 'outline'):
            raise PropellerError(
                'Parameter "style" should be "default", "raised", ' +
                '"flat", "outline" or empty  ("{}" given).'.format(style))
        else:
            classes = add_css_class(classes, 'pmd-btn-%s' % style)
        classes = add_css_class(classes, extra_classes)
        self.attrs['class'] = classes
        self.icon_content = render_icon(icon) if icon else ''
        if href:
            self.attrs['href'] = href
            self.tag = 'a'
        else:
            self.tag = 'button'
        if _id:
            self.attrs['id'] = _id
        if name:
            self.attrs['name'] = name
        if value:
            self.attrs['value'] = value
        if title:
            self.attrs['title'] = title

    def as_html(self):
        return render_tag(self.tag, attrs=self.attrs,
                          content=mark_safe(text_concat(self.icon_content, self.content, separator=' ')), )
