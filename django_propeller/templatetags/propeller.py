# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from math import floor

from django import template
from django.contrib.messages import constants as message_constants
from django.template import Context
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

from ..propeller import (
    css_url, javascript_url, jquery_url, theme_url, get_propeller_setting
)
from ..components import render_icon, render_alert, render_bootstrap_icon
from ..forms import (
    render_button, render_field, render_field_and_label, render_form,
    render_form_group, render_formset, render_fab,
    render_label, render_form_errors, render_formset_errors
)
from ..text import force_text
from ..utils import handle_var, parse_token_contents, url_replace_param
from ..utils import render_link_tag, render_tag, render_template_file

MESSAGE_LEVEL_CLASSES = {
    message_constants.DEBUG: "alert alert-warning",
    message_constants.INFO: "alert alert-info",
    message_constants.SUCCESS: "alert alert-success",
    message_constants.WARNING: "alert alert-warning",
    message_constants.ERROR: "alert alert-danger",
}

register = template.Library()


@register.filter
def propeller_setting(value):
    """
    A simple way to read Propeller settings in a template.

    Please consider this filter private for now, do not use it in your own
    templates.
    """
    return get_propeller_setting(value)


@register.filter
def propeller_message_classes(message):
    """Return the message classes for a message"""
    extra_tags = None
    try:
        extra_tags = message.extra_tags
    except AttributeError:
        pass
    if not extra_tags:
        extra_tags = ""
    classes = [extra_tags]
    try:
        level = message.level
    except AttributeError:
        pass
    else:
        try:
            classes.append(MESSAGE_LEVEL_CLASSES[level])
        except KeyError:
            classes.append("alert alert-danger")
    return ' '.join(classes).strip()


@register.simple_tag
def propeller_jquery_url():
    """
    Return the full url to jQuery file to use

    Default value: ``//code.jquery.com/jquery.min.js``

    This value is configurable, see Settings section

    **Tag name**::

        propeller_jquery_url

    **Usage**::

        {% propeller_jquery_url %}

    **Example**::

        {% propeller_jquery_url %}
    """
    return jquery_url()


@register.simple_tag
def propeller_javascript_url():
    """
    Return the full url to the Propeller JavaScript library

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        propeller_javascript_url

    **Usage**::

        {% propeller_javascript_url %}

    **Example**::

        {% propeller_javascript_url %}
    """
    return javascript_url()


@register.simple_tag
def propeller_css_url():
    """
    Return the full url to the Propeller CSS library

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        propeller_css_url

    **Usage**::

        {% propeller_css_url %}

    **Example**::

        {% propeller_css_url %}
    """
    return css_url()


@register.simple_tag
def propeller_theme_url():
    """
    Return the full url to a Propeller theme CSS library

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        propeller_theme_url

    **Usage**::

        {% propeller_theme_url %}

    **Example**::

        {% propeller_theme_url %}
    """
    return theme_url()


@register.simple_tag
def propeller_css():
    """
    Return HTML for Propeller CSS.

    Adjust url in settings. If no url is returned, we don't want this statement
    to return any HTML. This is intended behavior.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        propeller_css

    **Usage**::

        {% propeller_css %}

    **Example**::

        {% propeller_css %}
    """
    rendered_urls = [render_link_tag(propeller_css_url()), ]
    if propeller_theme_url():
        rendered_urls.append(render_link_tag(propeller_theme_url()))
    return mark_safe(''.join([url for url in rendered_urls]))


@register.simple_tag
def propeller_javascript(jquery=None):
    """
    Return HTML for Propeller JavaScript.

    Adjust url in settings. If no url is returned, we don't want this
    statement to return any HTML.
    This is intended behavior.

    Default value: ``None``

    This value is configurable, see Settings section

    **Tag name**::

        propeller_javascript

    **Parameters**:

        :jquery: Truthy to include jQuery as well as propeller

    **Usage**::

        {% propeller_javascript %}

    **Example**::

        {% propeller_javascript jquery=1 %}
    """
    javascript = ''
    # See if we have to include jQuery
    if jquery is None:
        jquery = get_propeller_setting('include_jquery', False)
    # NOTE: No async on scripts, not mature enough. See issue #52 and #56
    if jquery:
        url = propeller_jquery_url()
        if url:
            javascript += render_tag('script', attrs={'src': url})
    url = propeller_javascript_url()
    if url:
        attrs = {'src': url}
        javascript += render_tag('script', attrs=attrs)
    return mark_safe(javascript)


@register.simple_tag
def propeller_formset(*args, **kwargs):
    """
    Render a formset

    **Tag name**::

        propeller_formset

    **Parameters**:

        formset
            The formset that is being rendered


        See propeller_field_ for other arguments

    **Usage**::

        {% propeller_formset formset %}

    **Example**::

        {% propeller_formset formset layout='horizontal' %}

    """
    return render_formset(*args, **kwargs)


@register.simple_tag
def propeller_formset_errors(*args, **kwargs):
    """
    Render formset errors

    **Tag name**::

        propeller_formset_errors

    **Parameters**:

        formset
            The formset that is being rendered

        layout
            Context value that is available in the template ``propeller/form_errors.html`` as ``layout``.

    **Usage**::

        {% propeller_formset_errors formset %}

    **Example**::

        {% propeller_formset_errors formset layout='inline' %}
    """
    return render_formset_errors(*args, **kwargs)


@register.simple_tag
def propeller_form(*args, **kwargs):
    """
    Render a form

    **Tag name**::

        propeller_form

    **Parameters**:

        form
            The form that is to be rendered

        exclude
            A list of field names (comma separated) that should not be rendered
            E.g. exclude=subject,bcc

        See propeller_field_ for other arguments

    **Usage**::

        {% propeller_form form %}

    **Example**::

        {% propeller_form form layout='inline' %}
    """
    return render_form(*args, **kwargs)


@register.simple_tag
def propeller_form_errors(*args, **kwargs):
    """
    Render form errors

    **Tag name**::

        propeller_form_errors

    **Parameters**:

        form
            The form that is to be rendered

        type
            Control which type of errors should be rendered.

            One of the following values:

                * ``'all'``
                * ``'fields'``
                * ``'non_fields'``

            :default: ``'all'``

        layout
            Context value that is available in the template ``propeller/form_errors.html`` as ``layout``.

    **Usage**::

        {% propeller_form_errors form %}

    **Example**::

        {% propeller_form_errors form layout='inline' %}
    """
    return render_form_errors(*args, **kwargs)


@register.simple_tag
def propeller_field(*args, **kwargs):
    """
    Render a field

    **Tag name**::

        propeller_field

    **Parameters**:


        field
            The form field to be rendered

        layout
            If set to ``'horizontal'`` then the field and label will be rendered side-by-side, as long as there
            is no ``field_class`` set as well.

        form_group_class
            CSS class of the ``div`` that wraps the field and label.

            :default: ``'form-group'``

        field_class
            CSS class of the ``div`` that wraps the field.

        label_class
            CSS class of the ``label`` element. Will always have ``control-label`` as the last CSS class.

        show_help
            Show the field's help text, if the field has help text.

            :default: ``True``

        show_label
            Whether the show the label of the field.

            :default: ``True``

        exclude
            A list of field names that should not be rendered

        set_required
            When set to ``True`` and the field is required then the ``required`` attribute is set on the
            rendered field. This only works up to Django 1.8. Higher Django versions handle ``required``
            natively.

            :default: ``True``

        set_disabled
            When set to ``True`` then the ``disabled`` attribute is set on the rendered field. This only
            works up to Django 1.8.  Higher Django versions handle ``disabled`` natively.

            :default: ``False``

        size
            Controls the size of the rendered ``div.form-group`` through the use of CSS classes.

            One of the following values:

                * ``'small'``
                * ``'medium'``
                * ``'large'``

        placeholder
            Sets the placeholder text of a textbox

        horizontal_label_class
            Class used on the label when the ``layout`` is set to ``horizontal``.

            :default: ``'col-md-3'``. Can be changed in :doc:`settings`

        horizontal_field_class
            Class used on the field when the ``layout`` is set to ``horizontal``.

            :default: ``'col-md-9'``. Can be changed in :doc:`settings`

        addon_before
            Text that should be prepended to the form field.
            See the `propeller docs <http://getpropeller.com/components/#input-groups-basic>` for an example.

        addon_after
            Text that should be appended to the form field.
            See the `propeller docs <http://getpropeller.com/components/#input-groups-basic>` for an example.

        addon_before_class
            Class used on the span when ``addon_before`` is used.

            One of the following values:
                
                * ``'input-group-addon'``
                * ``'input-group-btn'``

            :default: ``input-group-addon``

        addon_after_class
            Class used on the span when ``addon_after`` is used.

            One of the following values:
                
                * ``'input-group-addon'``
                * ``'input-group-btn'``

            :default: ``input-group-addon``

        error_css_class
            CSS class used when the field has an error

            :default: ``'has-error'``. Can be changed :doc:`settings`

        required_css_class
            CSS class used on the ``div.form-group`` to indicate a field is required

            :default: ``''``. Can be changed :doc:`settings`

        bound_css_class
            CSS class used when the field is bound

            :default: ``'has-success'``. Can be changed :doc:`settings`

    **Usage**::

        {% propeller_field field %}

    **Example**::

        {% propeller_field field show_label=False %}
    """
    return render_field(*args, **kwargs)


@register.simple_tag()
def propeller_label(*args, **kwargs):
    """
    Render a label

    **Tag name**::

        propeller_label

    **Parameters**:

        content
            The label's text

        label_for
            The value that will be in the ``for`` attribute of the rendered ``<label>``

        label_class
            The CSS class for the rendered ``<label>``

        label_title
            The value that will be in the ``title`` attribute of the rendered ``<label>``

    **Usage**::

        {% propeller_label content %}

    **Example**::

        {% propeller_label "Email address" label_for="exampleInputEmail1" %}

    """
    return render_label(*args, **kwargs)


@register.simple_tag
def propeller_button(*args, **kwargs):
    """
    Render a button

    **Tag name**::

        propeller_button

    **Parameters**:

        content
            The text to be displayed in the button

        button_type
            Optional field defining what type of button this is.

            Accepts one of the following values:

                * ``'submit'``
                * ``'reset'``
                * ``'button'``
                * ``'link'``

        style
            Optional field defining which style button should have.

            Accepts one of the following values:

                * ``'default'``
                * ``'raised'``
                * ``'flat'``
                * ``'outline'``

        icon
            Name of an icon to render in the button's visible content. See propeller_icon_ for acceptable values.

        button_class
            The class of button to use. If none is given, btn-default will be used.

        extra_classes
            Any extra CSS classes that should be added to the button.

        size
            Optional field to control the size of the button.

            Accepts one of the following values:

                * ``'xs'``
                * ``'sm'``
                * ``'small'``
                * ``'md'``
                * ``'medium'``
                * ``'lg'``
                * ``'large'``


        href
            Render the button as an ``<a>`` element. The ``href`` attribute is set with this value.

        name
            Value of the ``name`` attribute of the rendered element.

        value
            Value of the ``value`` attribute of the rendered element.

    **Usage**::

        {% propeller_button content %}

    **Example**::

        {% propeller_button "Save" button_type="submit" button_class="btn-primary" %}
    """
    return render_button(*args, **kwargs)


@register.simple_tag
def propeller_fab(*args, **kwargs):
    """
    Render a floating action button

    **Tag name**::

        propeller_fab

    **Parameters**:

        content
            The text to be displayed in the button

        button_type
            Optional field defining what type of button this is.

            Accepts one of the following values:

                * ``'submit'``
                * ``'reset'``
                * ``'button'``
                * ``'link'``

        style
            Optional field defining which style button should have.

            Accepts one of the following values:

                * ``'default'``
                * ``'raised'``
                * ``'flat'``
                * ``'outline'``

        icon
            Name of an icon to render in the button's visible content. See propeller_icon_ for acceptable values.

        button_class
            The class of button to use. If none is given, btn-default will be used.

        extra_classes
            Any extra CSS classes that should be added to the button.

        size
            Optional field to control the size of the button.

            Accepts one of the following values:

                * ``'xs'``
                * ``'sm'``
                * ``'small'``
                * ``'md'``
                * ``'medium'``
                * ``'lg'``
                * ``'large'``


        href
            Render the button as an ``<a>`` element. The ``href`` attribute is set with this value.

        name
            Value of the ``name`` attribute of the rendered element.

        value
            Value of the ``value`` attribute of the rendered element.

    **Usage**::

        {% propeller_fab content %}

    **Example**::

        {% propeller_fab "Save" button_type="submit" button_class="btn-primary" %}
    """
    return render_fab(*args, **kwargs)


@register.simple_tag
def propeller_icon(icon, **kwargs):
    """
    Render an icon

    **Tag name**:

        propeller_icon

    **Parameters**:

        icon
            Icon name. See the `Propeller docs <http://propeller.in/style/icons.php>`_ for all icons.

        size
            Size of the icon. Must be one of 'xs', 'sm', 'md', or 'lg'. Default: 'sm'

        extra_classes
            Extra CSS classes to add to the icon HTML. Optional

        title
            A title for the icon (HTML title attrivute). Optional

    **Usage**::

        {% propeller_icon icon %}

    **Example**::

        {% propeller_icon "star" %}

    """
    return render_icon(icon, **kwargs)


@register.simple_tag
def propeller_bootstrap_icon(icon, **kwargs):
    """
    Render an icon

    **Tag name**:

        propeller_bootstrap_icon

    **Parameters**:

        icon
            Icon name. See the `Bootstrap docs <http://getbootstrap.com/components/#glyphicons>`_ for all icons.

        extra_classes
            Extra CSS classes to add to the icon HTML. Optional

        title
            A title for the icon (HTML title attrivute). Optional

    **Usage**::

        {% propeller_bootstrap_icon icon %}

    **Example**::

        {% propeller_bootstrap_icon "star" %}

    """
    return render_bootstrap_icon(icon, **kwargs)


@register.simple_tag
def propeller_alert(content, alert_type='info', dismissable=True):
    """
    Render an alert

    **Tag name**::

        propeller_alert

    **Parameters**:

        content
            HTML content of alert

        alert_type
            * ``'info'``
            * ``'warning'``
            * ``'danger'``
            * ``'success'``

            :default: ``'info'``

        dismissable
            boolean, is alert dismissable

            :default: ``True``

    **Usage**::

        {% propeller_alert content %}

    **Example**::

        {% propeller_alert "Something went wrong" alert_type='error' %}

    """
    return render_alert(content, alert_type, dismissable)


@register.tag('buttons')
def propeller_buttons(parser, token):
    """
    Render buttons for form

    **Tag name**::

        buttons

    **Parameters**:

        submit
            Text for a submit button

        reset
            Text for a reset button

    **Usage**::

        {% buttons %}{% endbuttons %}

    **Example**::

        {% buttons submit='OK' reset="Cancel" %}{% endbuttons %}

    """
    kwargs = parse_token_contents(parser, token)
    kwargs['nodelist'] = parser.parse(('endbuttons',))
    parser.delete_first_token()
    return ButtonsNode(**kwargs)


class ButtonsNode(template.Node):
    def __init__(self, nodelist, args, kwargs, asvar, **kwargs2):
        self.nodelist = nodelist
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        output_kwargs = {}
        for key in self.kwargs:
            output_kwargs[key] = handle_var(self.kwargs[key], context)
        buttons = []
        submit = output_kwargs.get('submit', None)
        reset = output_kwargs.get('reset', None)
        if submit:
            buttons.append(propeller_button(submit, 'submit'))
        if reset:
            buttons.append(propeller_button(reset, 'reset'))
        buttons = ' '.join(buttons) + self.nodelist.render(context)
        output_kwargs.update({
            'label': None,
            'field': buttons,
        })
        output = render_form_group(render_field_and_label(**output_kwargs))
        if self.asvar:
            context[self.asvar] = output
            return ''
        else:
            return output


@register.simple_tag(takes_context=True)
def propeller_messages(context, *args, **kwargs):
    """
    Show django.contrib.messages Messages in propeller alert containers.

    In order to make the alerts dismissable (with the close button),
    we have to set the jquery parameter too when using the
    propeller_javascript tag.

    Uses the template ``propeller/messages.html``.

    **Tag name**::

        propeller_messages

    **Parameters**:

        None.

    **Usage**::

        {% propeller_messages %}

    **Example**::

        {% propeller_javascript jquery=1 %}
        {% propeller_messages %}

    """
    # Force Django 1.8+ style, so dicts and not Context
    # TODO: This may be due to a bug in Django 1.8/1.9+
    if Context and isinstance(context, Context):
        context = context.flatten()
    context.update({'message_constants': message_constants})
    return render_template_file('propeller/messages.html', context=context)


@register.inclusion_tag('propeller/pagination.html')
def propeller_pagination(page, **kwargs):
    """
    Render pagination for a page

    **Tag name**::

        propeller_pagination

    **Parameters**:

        page
            The page of results to show.

        pages_to_show
            Number of pages in total

            :default: ``11``

        url
            URL to navigate to for pagination forward and pagination back.

            :default: ``None``

        size
            Controls the size of the pagination through CSS. Defaults to being normal sized.

            One of the following:

                * ``'small'``
                * ``'large'``

            :default: ``None``

        extra
            Any extra page parameters.

            :default: ``None``

        parameter_name
            Name of the paging URL parameter.

            :default: ``'page'``

    **Usage**::

        {% propeller_pagination page %}

    **Example**::

        {% propeller_pagination lines url="/pagination?page=1" size="large" %}

    """
    pagination_kwargs = kwargs.copy()
    pagination_kwargs['page'] = page
    return get_pagination_context(**pagination_kwargs)


@register.simple_tag
def propeller_url_replace_param(url, name, value):
    return url_replace_param(url, name, value)


def get_pagination_context(page, pages_to_show=11,
                           url=None, size=None, extra=None,
                           parameter_name='page'):
    """Generate propeller pagination context from a page object"""
    pages_to_show = int(pages_to_show)
    if pages_to_show < 1:
        raise ValueError(
            "Pagination pages_to_show should be a positive integer, you specified {pages}".format(
                pages=pages_to_show)
        )
    num_pages = page.paginator.num_pages
    current_page = page.number
    half_page_num = int(floor(pages_to_show / 2))
    if half_page_num < 0:
        half_page_num = 0
    first_page = current_page - half_page_num
    if first_page <= 1:
        first_page = 1
    if first_page > 1:
        pages_back = first_page - half_page_num
        if pages_back < 1:
            pages_back = 1
    else:
        pages_back = None
    last_page = first_page + pages_to_show - 1
    if pages_back is None:
        last_page += 1
    if last_page > num_pages:
        last_page = num_pages
    if last_page < num_pages:
        pages_forward = last_page + half_page_num
        if pages_forward > num_pages:
            pages_forward = num_pages
    else:
        pages_forward = None
        if first_page > 1:
            first_page -= 1
        if pages_back is not None and pages_back > 1:
            pages_back -= 1
        else:
            pages_back = None
    pages_shown = []
    for i in range(first_page, last_page + 1):
        pages_shown.append(i)
        # Append proper character to url
    if url:
        # Remove existing page GET parameters
        url = force_text(url)
        url = re.sub(r'\?{0}\=[^\&]+'.format(parameter_name), '?', url)
        url = re.sub(r'\&{0}\=[^\&]+'.format(parameter_name), '', url)
        # Append proper separator
        if '?' in url:
            url += '&'
        else:
            url += '?'
            # Append extra string to url
    if extra:
        if not url:
            url = '?'
        url += force_text(extra) + '&'
    if url:
        url = url.replace('?&', '?')
    # Set CSS classes, see http://getpropeller.com/components/#pagination
    pagination_css_classes = ['pagination']
    if size == 'small':
        pagination_css_classes.append('pagination-sm')
    elif size == 'large':
        pagination_css_classes.append('pagination-lg')
        # Build context object
    return {
        'propeller_pagination_url': url,
        'num_pages': num_pages,
        'current_page': current_page,
        'first_page': first_page,
        'last_page': last_page,
        'pages_shown': pages_shown,
        'pages_back': pages_back,
        'pages_forward': pages_forward,
        'pagination_css_classes': ' '.join(pagination_css_classes),
        'parameter_name': parameter_name,
    }


@register.filter(needs_autoescape=True)
def pmd_muted_text(text, autoescape=True):
    """
    Render a muted text (secondary heading).

    **Tag name**::

        pmd_muted_text

    **Usage**::

        {{ text_variable|pmd_muted_text }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<span class="text-muted">%s</span>' % esc(text)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def pmd_display_text(text, size=1, autoescape=True):
    """
    Render text as a Propeller display text (heading).

    **Tag name**::

        pmd_display_text

    **Parameters**::

        size
            Controls the size of the heading.

            An integer from 1 (normal) to 4 (very large)

            :default: ``1``

    **Usage**::

        {{ text_variable|pmd_display_text:size }}

    **Example**::

        {{ my_text|pmd_display_text:3 }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<span class="pmd-display%d">%s</span>' % (int(size), esc(text))
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def pmd_lead_text(text, autoescape=True):
    """
    Render text as a Propeller lead text (intro).

    **Tag name**::

        pmd_lead_text

    **Usage**::

        {{ text_variable|pmd_lead_text }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<span class="lead">%s</span>' % esc(text)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def pmd_mark_text(text, autoescape=True):
    """
    Render highligthed text.

    **Tag name**::

        pmd_mark_text

    **Usage**::

        {{ text_variable|pmd_mark_text }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<mark>%s</mark>' % esc(text)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def pmd_strike_text(text, autoescape=True):
    """
    Render striked text.

    **Tag name**::

        pmd_strike_text

    **Usage**::

        {{ text_variable|pmd_strike_text }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<s>%s</s>' % esc(text)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def pmd_underline_text(text, autoescape=True):
    """
    Render underlined text.

    **Tag name**::

        pmd_underline_text

    **Usage**::

        {{ text_variable|pmd_underline_text }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<u>%s</u>' % esc(text)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def pmd_bold_text(text, autoescape=True):
    """
    Render bold text.

    **Tag name**::

        pmd_bold_text

    **Usage**::

        {{ text_variable|pmd_bold_text }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<strong>%s</strong>' % esc(text)
    return mark_safe(result)


@register.filter(needs_autoescape=True)
def pmd_italic_text(text, autoescape=True):
    """
    Render italic text.

    **Tag name**::

        pmd_italic_text

    **Usage**::

        {{ text_variable|pmd_italic_text }}
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = '<em>%s</em>' % esc(text)
    return mark_safe(result)


@register.simple_tag
def propeller_navbar(navbar):
    """
    Render a navbar.

    **Tag name**::

        propeller_navbar

    **Parameters**:

        navbar
            The previously defined navbar instance

    **Usage**::

        {% propeller_navbar navbar_instance %}
    """
    return navbar.as_html()


@register.simple_tag
def propeller_card(card):
    """
    Render a propeller card.

    **Tag name**::

        propeller_card

    **Parameters**:

        card
            The previously defined card instance

    **Usage**::

        {% propeller_card card_instance %}
    """
    return card.as_html()
