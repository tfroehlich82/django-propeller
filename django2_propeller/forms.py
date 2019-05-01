# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.widgets import AdminFileWidget
from django.forms import (
    HiddenInput, FileInput, CheckboxSelectMultiple, Textarea, TextInput,
    PasswordInput
)
from django.forms.widgets import CheckboxInput
from django.utils.safestring import mark_safe

from .propeller import (
    get_propeller_setting, get_form_renderer, get_field_renderer,
    get_formset_renderer,
    PROPELLER_SET_REQUIRED_SET_DISABLED
)
from .components import Button, FAB
from .utils import add_css_class, render_tag

FORM_GROUP_CLASS = 'form-group pmd-textfield'


def render_formset(formset, **kwargs):
    """
    Render a formset to a Bootstrap layout
    """
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render()


def render_formset_errors(formset, **kwargs):
    """
    Render formset errors to a Bootstrap layout
    """
    renderer_cls = get_formset_renderer(**kwargs)
    return renderer_cls(formset, **kwargs).render_errors()


def render_form(form, **kwargs):
    """Render a form to a Bootstrap layout"""
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render()


def render_form_errors(form, _type='all', **kwargs):
    """Render form errors to a Bootstrap layout"""
    renderer_cls = get_form_renderer(**kwargs)
    return renderer_cls(form, **kwargs).render_errors(_type)


def render_field(field, **kwargs):
    """Render a field to a Bootstrap layout"""
    renderer_cls = get_field_renderer(**kwargs)
    return renderer_cls(field, **kwargs).render()


def render_label(content, label_for=None, label_class=None, label_title=''):
    """Render a label with content"""
    attrs = {}
    if label_for:
        attrs['for'] = label_for
    if label_class:
        attrs['class'] = label_class
    if label_title:
        attrs['title'] = label_title
    return render_tag('label', attrs=attrs, content=content)


def render_button(content, button_type=None, icon=None, button_class='btn-default', size='',
                  href='', name=None, value=None, title=None, style='default', extra_classes='', _id=''):
    """Render a button with content"""
    return Button(content, button_type, icon, button_class, size, href, name, value, title,
                  style, extra_classes, _id).as_html()


def render_fab(content, button_type=None, icon=None, button_class='btn-default', size='', href='',
               name=None, value=None, title=None, style='default', extra_classes='', _id=''):
    """Render a button with content"""
    return FAB(content, button_type, icon, button_class, size, href, name, value, title,
               style, extra_classes, _id).as_html()


def render_field_and_label(
        field, label, field_class='', label_for=None, label_class='',
        layout='', **kwargs):
    """Render a field with its label"""
    if layout == 'horizontal':
        if not label_class:
            label_class = get_propeller_setting('horizontal_label_class')
        if not field_class:
            field_class = get_propeller_setting('horizontal_field_class')
        if not label:
            label = mark_safe('&#160;')
        label_class = add_css_class(label_class, 'control-label')
    html = field
    if field_class:
        html = '<div class="{klass}">{html}</div>'.format(
            klass=field_class, html=html)
    if label:
        html = render_label(
            label, label_for=label_for, label_class=label_class) + html
    return html


def render_form_group(content, css_class=FORM_GROUP_CLASS):
    """Render a Bootstrap form group"""
    return '<div class="{klass}">{content}</div>'.format(
        klass=css_class,
        content=content,
    )


def is_widget_required_attribute(widget):
    """Is this widget required?"""
    if PROPELLER_SET_REQUIRED_SET_DISABLED and not get_propeller_setting('set_required'):
        return False
    if not widget.is_required:
        return False
    if isinstance(
            widget, (
                    AdminFileWidget, HiddenInput, FileInput,
                    CheckboxInput, CheckboxSelectMultiple)):
        return False
    return True


def is_widget_with_placeholder(widget):
    """
    Is this a widget that should have a placeholder?
    Only text, search, url, tel, e-mail, password, number have placeholders
    These are all derived form TextInput, except for Textarea
    """
    # PasswordInput inherits from Input in Django 1.4.
    # It was changed to inherit from TextInput in 1.5.
    return isinstance(widget, (TextInput, Textarea, PasswordInput))
