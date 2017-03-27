# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.forms.formsets import formset_factory
from django.template import Context, Template
from django.test import TestCase
from django.core.urlresolvers import NoReverseMatch

from .propeller import PROPELLER_SET_REQUIRED_SET_DISABLED
from .exceptions import PropellerError, PropellerException
from .text import text_value, text_concat
from .utils import add_css_class, render_tag
from .test_data import DemoCard1, DemoCard2, DemoCard3, DemoCard4, TestNavbar1, TestNavbar2, TestNavbar3, \
    NavBarLinkItem, NavBarDropDownDivider, NavBarDropDownItem, NavBar, TestNavbar4, DemoMediaImage1, DemoMediaImage3, \
    DemoMedia1, DemoMedia2, DemoMedia3, DemoCard5, DemoMedia4, DemoMedia5
from .test_results import RESULT_CARD1, RESULT_CARD2, RESULT_CARD3, RESULT_CARD4, RESULT_NAVBAR1, RESULT_NAVBAR2, \
    RESULT_NAVBAR3, RESULT_CARD5

try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser


class TemplateTestCase(TestCase):

    @staticmethod
    def render_template(string, context=None):
        context = context or {}
        context = Context(context)
        return Template(string).render(context)

    def render_template_with_propeller(self, string, context=None):
        return self.render_template('{% load propeller %}' + string, context)

    def render_template_with_form(self, text, context=None):
        """
        Create a template ``text`` that first loads bootstrap3.
        """
        if not context:
            context = {}
        if 'form' not in context:
            context['form'] = TestForm()
        return self.render_template_with_propeller(text, context)

    def render_formset(self, formset=None, context=None):
        """
        Create a template that renders a formset
        """
        if not context:
            context = {}
        context['formset'] = formset
        return self.render_template_with_form('{% propeller_formset formset %}', context)

    def render_form(self, form=None, context=None):
        """
        Create a template that renders a form
        """
        if not context:
            context = {}
        if form:
            context['form'] = form
        return self.render_template_with_form('{% propeller_form form %}', context)

    def render_form_field(self, field, context=None):
        """
        Create a template that renders a field
        """
        form_field = 'form.%s' % field
        return self.render_template_with_form('{% propeller_field ' + form_field + ' %}', context)

    def render_field(self, field, context=None):
        """
        Create a template that renders a field
        """
        if not context:
            context = {}
        context['field'] = field
        return self.render_template_with_form('{% propeller_field field %}', context)

    def get_title_from_html(self, html):
        class GetTitleParser(HTMLParser):
            def __init__(self):
                HTMLParser.__init__(self)
                self.title = None

            def handle_starttag(self, tag, attrs):
                for attr, value in attrs:
                    if attr == 'title':
                        self.title = value

        parser = GetTitleParser()
        parser.feed(html)

        return parser.title


TestCase = TemplateTestCase


RADIO_CHOICES = (
    ('1', 'Radio 1'),
    ('2', 'Radio 2'),
)

MEDIA_CHOICES = (
    ('Audio', (
        ('vinyl', 'Vinyl'),
        ('cd', 'CD'),
    )
     ),
    ('Video', (
        ('vhs', 'VHS Tape'),
        ('dvd', 'DVD'),
    )
     ),
    ('unknown', 'Unknown'),
)


class TestForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    date = forms.DateField(required=False)
    datetime = forms.SplitDateTimeField(widget=AdminSplitDateTime(), required=False)
    subject = forms.CharField(
        max_length=100,
        help_text='my_help_text',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'placeholdertest'}),
    )
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text='<i>my_help_text</i>')
    sender = forms.EmailField(
        label='Sender © unicode',
        help_text='E.g., "me@example.com"')
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(
        required=False,
        help_text='cc stands for "carbon copy." You will get a copy in your mailbox.'
    )
    select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    select2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        help_text='Check as many as you like.',
    )
    select3 = forms.ChoiceField(choices=MEDIA_CHOICES)
    select4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        help_text='Check as many as you like.',
    )
    category1 = forms.ChoiceField(
        choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )
    category3 = forms.ChoiceField(
        widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )
    addon = forms.CharField(
        widget=forms.TextInput(attrs={'addon_before': 'before', 'addon_after': 'after'}),
    )

    required_css_class = 'bootstrap3-req'

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        # return cleaned_data


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = ''


class SettingsTest(TestCase):
    def test_settings(self):
        from .propeller import PROPELLER
        self.assertTrue(PROPELLER)

    def test_propeller_javascript_tag(self):
        res = self.render_template_with_form('{% propeller_javascript %}')
        self.assertEqual(
            res.strip(),
            '<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>'
        )

    def test_propeller_css_tag(self):
        res = self.render_template_with_form('{% propeller_css %}').strip()
        self.assertIn(
            '<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">',
            res
        )

    # def test_settings_filter(self):
    #     res = self.render_template_with_form('{{ "required_css_class"|propeller_setting }}')
    #     self.assertEqual(res.strip(), 'bootstrap3-req')
    #     res = self.render_template_with_form('{% if "javascript_in_head"|propeller_setting %}head{% else %}body{% endif %}')
    #     self.assertEqual(res.strip(), 'head')

    def test_required_class(self):
        form = TestForm()
        res = self.render_template_with_form('{% propeller_form form %}', {'form': form})
        self.assertIn('bootstrap3-req', res)

    # def test_error_class(self):
    #     form = TestForm({})
    #     res = self.render_template_with_form('{% propeller_form form %}', {'form': form})
    #     self.assertIn('bootstrap3-err', res)

    # def test_bound_class(self):
    #     form = TestForm({'sender': 'sender'})
    #     res = self.render_template_with_form('{% propeller_form form %}', {'form': form})
    #     self.assertIn('bootstrap3-bound', res)


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = self.render_template_with_form('')
        self.assertEqual(res.strip(), '')

    def test_text_template(self):
        res = self.render_template_with_form('some text')
        self.assertEqual(res.strip(), 'some text')

    def test_propeller_template(self):
        res = self.render_template(
            '{% extends "propeller/propeller.html" %}' +
            '{% block propeller_content %}' +
            'test_propeller_content' +
            '{% endblock %}'
        )
        self.assertIn('test_propeller_content', res)

    def test_javascript_without_jquery(self):
        res = self.render_template_with_form('{% propeller_javascript jquery=0 %}')
        self.assertIn('bootstrap', res)
        self.assertNotIn('jquery', res)

    def test_javascript_with_jquery(self):
        res = self.render_template_with_form('{% propeller_javascript jquery=1 %}')
        self.assertIn('bootstrap', res)
        self.assertIn('jquery', res)


class FormSetTest(TestCase):
    def test_illegal_formset(self):
        with self.assertRaises(PropellerError):
            self.render_formset(formset='illegal')


class FormTest(TestCase):
    def test_illegal_form(self):
        with self.assertRaises(PropellerError):
            self.render_form(form='illegal')

    def test_field_names(self):
        form = TestForm()
        res = self.render_form(form)
        for field in form:
            # datetime has a multiwidget field widget
            if field.name == "datetime":
                self.assertIn('name="datetime_0"', res)
                self.assertIn('name="datetime_1"', res)
            else:
                self.assertIn('name="%s"' % field.name, res)

    def test_field_addons(self):
        form = TestForm()
        res = self.render_form(form)
        self.assertIn('<div class="input-group"><span class="input-group-addon">before</span><input', res)
        self.assertIn('/><span class="input-group-addon">after</span></div>', res)

    def test_exclude(self):
        form = TestForm()
        res = self.render_template_with_form(
            '{% propeller_form form exclude="cc_myself" %}', {'form': form})
        self.assertNotIn('cc_myself', res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = self.render_template_with_form(
            '{% propeller_form form layout="horizontal" %}', {'form': form})
        self.assertIn('col-md-3', res)
        self.assertIn('col-md-9', res)
        res = self.render_template_with_form(
            '{% propeller_form form layout="horizontal" ' +
            'horizontal_label_class="hlabel" ' +
            'horizontal_field_class="hfield" %}',
            {'form': form}
        )
        self.assertIn('hlabel', res)
        self.assertIn('hfield', res)

    def test_buttons_tag(self):
        form = TestForm()
        res = self.render_template_with_form(
            '{% buttons layout="horizontal" %}{% endbuttons %}', {'form': form})
        self.assertIn('col-md-3', res)
        self.assertIn('col-md-9', res)

    # def test_error_class(self):
    #     form = TestForm({'sender': 'sender'})
    #     res = render_template_with_form('{% propeller_form form %}', {'form': form})
    #     self.assertIn('bootstrap3-err', res)
    #
    #     res = render_template_with_form(
    #         '{% propeller_form form error_css_class="successful-test" %}',
    #         {'form': form}
    #     )
    #     self.assertIn('successful-test', res)
    #
    #     res = render_template_with_form('{% propeller_form form error_css_class="" %}',
    #                                     {'form': form})
    #     self.assertNotIn('bootstrap3-err', res)

    def test_required_class(self):
        form = TestForm({'sender': 'sender'})
        res = self.render_template_with_form('{% propeller_form form %}', {'form': form})
        self.assertIn('bootstrap3-req', res)

        res = self.render_template_with_form(
            '{% propeller_form form required_css_class="successful-test" %}',
            {'form': form}
        )
        self.assertIn('successful-test', res)

        res = self.render_template_with_form('{% propeller_form form required_css_class="" %}',
                                        {'form': form})
        self.assertNotIn('bootstrap3-req', res)

    # def test_bound_class(self):
    #     form = TestForm({'sender': 'sender'})
    #
    #     res = render_template_with_form('{% propeller_form form %}', {'form': form})
    #     self.assertIn('bootstrap3-bound', res)
    #
    #     res = render_template_with_form(
    #         '{% propeller_form form bound_css_class="successful-test" %}',
    #         {'form': form}
    #     )
    #     self.assertIn('successful-test', res)
    #
    #     res = render_template_with_form(
    #         '{% propeller_form form bound_css_class="" %}',
    #         {'form': form}
    #     )
    #     self.assertNotIn('bootstrap3-bound', res)


class FieldTest(TestCase):
    def test_illegal_field(self):
        with self.assertRaises(PropellerError):
            self.render_field(field='illegal')

    def test_show_help(self):
        res = self.render_form_field('subject')
        self.assertIn('my_help_text', res)
        self.assertNotIn('<i>my_help_text</i>', res)
        res = self.render_template_with_form('{% propeller_field form.subject show_help=0 %}')
        self.assertNotIn('my_help_text', res)

    def test_help_with_quotes(self):
        # Checkboxes get special handling, so test a checkbox and something else
        res = self.render_form_field('sender')
        self.assertEqual(self.get_title_from_html(res), TestForm.base_fields['sender'].help_text)
        res = self.render_form_field('cc_myself')
        self.assertEqual(self.get_title_from_html(res), TestForm.base_fields['cc_myself'].help_text)

    def test_subject(self):
        res = self.render_form_field('subject')
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_password(self):
        res = self.render_form_field('password')
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    def test_required_field(self):
        if PROPELLER_SET_REQUIRED_SET_DISABLED:
            required_field = self.render_form_field('subject')
            self.assertIn('required', required_field)
            self.assertIn('bootstrap3-req', required_field)
            not_required_field = self.render_form_field('message')
            self.assertNotIn('required', not_required_field)
            # Required field with required=0
            form_field = 'form.subject'
            rendered = self.render_template_with_form('{% propeller_field ' + form_field + ' set_required=0 %}')
            self.assertNotIn('required', rendered)
        else:
            required_css_class = 'bootstrap3-req'
            required_field = self.render_form_field('subject')
            self.assertIn(required_css_class, required_field)
            not_required_field = self.render_form_field('message')
            self.assertNotIn(required_css_class, not_required_field)
        # Required settings in field
        form_field = 'form.subject'
        rendered = self.render_template_with_form(
            '{% propeller_field ' + form_field + ' required_css_class="test-required" %}'
        )
        self.assertIn('test-required', rendered)

    def test_empty_permitted(self):
        """
        If a form has empty_permitted, no fields should get the CSS class for required.
        Django <= 1.8, also check `required` attribute.
        """
        if PROPELLER_SET_REQUIRED_SET_DISABLED:
            required_css_class = 'bootstrap3-req'
            form = TestForm()
            res = self.render_form_field('subject', {'form': form})
            self.assertIn(required_css_class, res)
            form.empty_permitted = True
            res = self.render_form_field('subject', {'form': form})
            self.assertNotIn(required_css_class, res)
        else:
            required_css_class = 'bootstrap3-req'
            form = TestForm()
            res = self.render_form_field('subject', {'form': form})
            self.assertIn(required_css_class, res)
            form.empty_permitted = True
            res = self.render_form_field('subject', {'form': form})
            self.assertNotIn(required_css_class, res)

    def test_input_group(self):
        res = self.render_template_with_form('{% propeller_field form.subject addon_before="$"  addon_after=".00" %}')
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-addon">$', res)
        self.assertIn('class="input-group-addon">.00', res)

    def test_input_group_addon_button(self):
        res = self.render_template_with_form(
            '{% propeller_field form.subject addon_before="$" addon_before_class="input-group-btn" '
            'addon_after=".00" addon_after_class="input-group-btn" %}'
        )
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-btn">$', res)
        self.assertIn('class="input-group-btn">.00', res)

    def test_size(self):
        def _test_size(param, klass):
            res = self.render_template_with_form('{% propeller_field form.subject size="' + param + '" %}')
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = self.render_template_with_form('{% propeller_field form.subject size="' + param + '" %}')
            self.assertNotIn('input-lg', res)
            self.assertNotIn('input-sm', res)
            self.assertNotIn('input-md', res)

        _test_size('sm', 'input-sm')
        _test_size('small', 'input-sm')
        _test_size('lg', 'input-lg')
        _test_size('large', 'input-lg')
        _test_size_medium('md')
        _test_size_medium('medium')
        _test_size_medium('')

    def test_datetime(self):
        field = self.render_form_field('datetime')
        self.assertIn('vDateField', field)
        self.assertIn('vTimeField', field)

    def test_field_same_render(self):
        context = dict(form=TestForm())
        rendered_a = self.render_form_field("addon", context)
        rendered_b = self.render_form_field("addon", context)
        self.assertEqual(rendered_a, rendered_b)

    def test_label(self):
        res = self.render_template_with_form('{% propeller_label "foobar" label_for="subject" %}')
        self.assertEqual('<label for="subject">foobar</label>', res)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields['addon'].widget.attrs.copy()
        context = dict(form=form)
        field_alone = self.render_form_field("addon", context)
        self.assertEqual(attrs, form.fields['addon'].widget.attrs)


class ComponentsTest(TestCase):
    def test_icon(self):
        res = self.render_template_with_form('{% propeller_icon "star" %}')
        self.assertEqual(
            res.strip(), '<i class="material-icons pmd-sm">star</i>')
        res = self.render_template_with_form('{% propeller_icon "star" title="alpha centauri" %}')
        self.assertIn(res.strip(), [
            '<i class="material-icons pmd-sm" title="alpha centauri">star</i>',
            '<span title="alpha centauri" class="glyphicon glyphicon-star"></span>',
        ])

    def test_alert(self):
        res = self.render_template_with_form('{% propeller_alert "content" alert_type="danger" %}')
        self.assertEqual(
            res.strip(),
            '<div class="alert alert-danger alert-dismissable">' +
            '<button type="button" class="close" data-dismiss="alert" ' +
            'aria-hidden="true">' +
            '&times;</button>content</div>'
        )


class MessagesTest(TestCase):
    def test_messages(self):
        class FakeMessage(object):
            """
            Follows the `django.contrib.messages.storage.base.Message` API.
            """
            level = None
            message = None
            extra_tags = None

            def __init__(self, level, message, extra_tags=None):
                self.level = level
                self.extra_tags = extra_tags
                self.message = message

            def __str__(self):
                return self.message

        pattern = re.compile(r'\s+')
        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        res = self.render_template_with_form(
            '{% propeller_messages messages %}', {'messages': messages})
        expected = """
    <div class="alert alert-warning alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        res = self.render_template_with_form(
            '{% propeller_messages messages %}', {'messages': messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """
        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )

        messages = [FakeMessage(None, "hello")]
        res = self.render_template_with_form(
            '{% propeller_messages messages %}', {'messages': messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello
    </div>
        """

        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")]
        res = self.render_template_with_form(
            '{% propeller_messages messages %}', {'messages': messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&#215;</button>
        hello http://example.com
    </div>        """
        self.assertEqual(
            re.sub(pattern, '', res).replace('rel="nofollow"', ''),
            re.sub(pattern, '', expected).replace('rel="nofollow"', '')
        )

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        res = self.render_template_with_form(
            '{% propeller_messages messages %}', {'messages': messages})
        expected = """
    <div class="alert alert-danger alert-dismissable">
        <button type="button" class="close" data-dismiss="alert"
            aria-hidden="true">&#215;</button>
        hello there
    </div>
        """
        self.assertEqual(
            re.sub(pattern, '', res),
            re.sub(pattern, '', expected)
        )


class UtilsTest(TestCase):
    def test_add_css_class(self):
        css_classes = "one two"
        css_class = "three four"
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, "three four one two")

    def test_text_value(self):
        self.assertEqual(text_value(''), "")
        self.assertEqual(text_value(' '), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator='='), "1=2")
        self.assertEqual(text_concat(None, 2, separator='='), "2")

    def test_render_tag(self):
        self.assertEqual(render_tag('span'), '<span></span>')
        self.assertEqual(render_tag('span', content='foo'), '<span>foo</span>')
        self.assertEqual(
            render_tag('span', attrs={'bar': 123}, content='foo'),
            '<span bar="123">foo</span>'
        )


class ButtonTest(TestCase):
    def test_button(self):
        res = self.render_template_with_form("{% propeller_button 'button' size='lg' %}")
        self.assertEqual('<button class="btn btn-default pmd-ripple-effect btn-lg pmd-btn-default" type="button">'
                         'button</button>', res.strip())
        res = self.render_template_with_form("{% propeller_button 'button' size='lg' href='#' %}")
        self.assertIn('<a class="btn btn-default pmd-ripple-effect btn-lg pmd-btn-default" href="#" type="button">'
                      'button</a>', res.strip())


class ShowLabelTest(TestCase):
    def test_show_label(self):
        form = TestForm()
        res = self.render_template_with_form(
            '{% propeller_form form show_label=False %}',
            {'form': form}
        )
        self.assertIn('sr-only', res)

    def test_for_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        test_formset = TestFormSet()
        res = self.render_template_with_form(
            '{% propeller_formset formset show_label=False %}',
            {'formset': test_formset}
        )
        self.assertIn('sr-only', res)

    def test_button_with_icon(self):
        res = self.render_template_with_form(
            "{% propeller_button 'test' icon='info-sign' %}"
        )
        self.assertEqual('<button class="btn btn-default pmd-ripple-effect pmd-btn-default" href="#" type="button">'
                         '<i class="material-icons pmd-sm">info-sign</i> test</button>', res.strip())
        res = self.render_template_with_form(
            "{% propeller_button 'test' icon='info-sign' button_class='btn-primary' %}"
        )
        self.assertEqual('<button class="btn btn-primary pmd-ripple-effect pmd-btn-default" href="#" type="button">'
                         '<i class="material-icons pmd-sm">info-sign</i> test</button>', res.strip())
        res = self.render_template_with_form(
            "{% propeller_button 'test' icon='info-sign' button_type='submit' %}"
        )
        self.assertEqual('<button class="btn btn-default pmd-ripple-effect pmd-btn-default" href="#" type="submit">'
                         '<i class="material-icons pmd-sm">info-sign</i> test</button>', res.strip())


class TypographyTest(TestCase):
    def test_marked_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_mark_text }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<mark>This is a test</mark>', res)

    def test_striked_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_strike_text }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<s>This is a test</s>', res)

    def test_underlined_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_underline_text }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<u>This is a test</u>', res)

    def test_bold_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_bold_text }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<strong>This is a test</strong>', res)

    def test_italic_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_italic_text }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<em>This is a test</em>', res)

    def test_lead_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_lead_text }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<span class="lead">This is a test</span>', res)

    def test_display_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_display_text:1 }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<span class="pmd-display1">This is a test</span>', res)
        res = self.render_template_with_propeller(
            '{{ text|pmd_display_text:2 }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<span class="pmd-display2">This is a test</span>', res)
        res = self.render_template_with_propeller(
            '{{ text|pmd_display_text:3 }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<span class="pmd-display3">This is a test</span>', res)
        res = self.render_template_with_propeller(
            '{{ text|pmd_display_text:4 }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<span class="pmd-display4">This is a test</span>', res)

    def test_muted_text_filter(self):
        res = self.render_template_with_propeller(
            '{{ text|pmd_muted_text }}',
            {'text': 'This is a test'}
        )
        self.assertInHTML('<span class="text-muted">This is a test</span>', res)


class FABsTests(TestCase):
    def test_default_fab(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="star" %}',
        )
        self.assertInHTML('<button class="btn pmd-btn-fab pmd-btn-default pmd-ripple-effect btn-default" type="button">'
                          '<i class="material-icons pmd-sm">star</i></button>', res)

    def test_default_fab_with_btn_class(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="warning" button_class="btn-warning" %}',
        )
        self.assertInHTML('<button class="btn btn-warning pmd-btn-fab pmd-ripple-effect pmd-btn-default" type="button">'
                          '<i class="material-icons pmd-sm">warning</i></button>', res)

    def test_default_fab_with_link(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "Link" button_class="btn-link" %}',
        )
        self.assertInHTML('<button class="btn pmd-btn-fab pmd-btn-default pmd-ripple-effect btn-link" type="button">'
                          'Link</button>', res)

    def test_raised_fab(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="star" style="raised" %}',
        )
        self.assertInHTML('<button class="btn btn-default pmd-btn-fab pmd-ripple-effect pmd-btn-raised" type="button">'
                          '<i class="material-icons pmd-sm">star</i></button>', res)

    def test_raised_fab_with_btn_class(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="error" style="raised" button_class="btn-danger" %}',
        )
        self.assertInHTML('<button class="btn btn-danger pmd-btn-fab pmd-ripple-effect pmd-btn-raised" type="button">'
                          '<i class="material-icons pmd-sm">error</i></button>', res)

    def test_raised_fab_with_link(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "Link" style="raised" button_class="btn-link" %}',
        )
        self.assertInHTML('<button class="btn btn-link pmd-btn-fab pmd-ripple-effect pmd-btn-raised" type="button">'
                          'Link</button>', res)

    def test_flat_fab(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="star" style="flat" %}',
        )
        self.assertInHTML('<button class="btn btn-default pmd-btn-fab pmd-ripple-effect pmd-btn-flat" type="button">'
                          '<i class="material-icons pmd-sm">star</i></button>', res)

    def test_flat_fab_with_btn_class(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="info" style="flat" button_class="btn-danger" %}',
        )
        self.assertInHTML('<button class="btn btn-danger pmd-btn-fab pmd-ripple-effect pmd-btn-flat" type="button">'
                          '<i class="material-icons pmd-sm">info</i></button>', res)

    def test_flat_fab_with_link(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "Link" style="flat" button_class="btn-link" %}',
        )
        self.assertInHTML('<button class="btn btn-link pmd-btn-fab pmd-ripple-effect pmd-btn-flat" type="button">'
                          'Link</button>', res)

    def test_outline_fab(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="star" style="outline" %}',
        )
        self.assertInHTML('<button class="btn btn-default pmd-btn-fab pmd-ripple-effect pmd-btn-outline" type="button">'
                          '<i class="material-icons pmd-sm">star</i></button>', res)

    def test_outline_fab_with_btn_class(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "" icon="check" style="outline" button_class="btn-danger" %}',
        )
        self.assertInHTML('<button class="btn btn-danger pmd-btn-fab pmd-ripple-effect pmd-btn-outline" type="button">'
                          '<i class="material-icons pmd-sm">check</i></button>', res)

    def test_outline_fab_with_link(self):
        res = self.render_template_with_propeller(
            '{% propeller_fab "Link" style="outline" button_class="btn-link" %}',
        )
        self.assertInHTML('<button class="btn btn-link pmd-btn-fab pmd-ripple-effect pmd-btn-outline" type="button">'
                          'Link</button>', res)


class DjangoAppTests(TestCase):
    def test_app_config(self):
        from django_propeller.apps import DjangoPropellerConfig
        self.assertEqual(DjangoPropellerConfig.name, 'django_propeller')


class PropellerMixinTests(TestCase):
    class TestNavbar(NavBar):
        pass

    def test_navbar_mixin(self):
        from django_propeller.views import NavBarMixin, ContextMixin
        test_mixin = NavBarMixin()
        self.assertIsInstance(test_mixin, ContextMixin)
        test_mixin.navbar_class = self.TestNavbar
        self.assertIsInstance(test_mixin.get_context_data().get('navbar')(), self.TestNavbar)


class PropellerNavBarTests(TestCase):
    def test_navbar_config(self):
        self.assertEqual(TestNavbar1().get_brand_url(), 'https://github.com/tfroehlich82/django-propeller')
        self.assertEqual(TestNavbar1().brandname, 'propeller-test')
        self.assertEqual(TestNavbar2().get_brand_url(), 'javascript:void(0);')
        with self.assertRaises(NoReverseMatch):
            TestNavbar4().get_brand_url()

    def test_rendered_template(self):
        res = self.render_template_with_propeller(
            '{% propeller_navbar testnav1 %}',
            context={'testnav1': TestNavbar1()}
        )
        self.assertInHTML(RESULT_NAVBAR1, res)
        res = self.render_template_with_propeller(
            '{% propeller_navbar testnav2 %}',
            context={'testnav2': TestNavbar2()}
        )
        self.assertInHTML(RESULT_NAVBAR2, res)
        res = self.render_template_with_propeller(
            '{% propeller_navbar testnav3 %}', {'testnav3': TestNavbar3()}
        )
        self.assertInHTML(RESULT_NAVBAR3, res)

    def test_navbar_items(self):
        for itm in TestNavbar4().items:
            if itm.name in ('Test1', ):
                self.assertIsInstance(itm, NavBarLinkItem)
                self.assertEqual(itm.get_url(), 'http://example.org')
            elif itm.name in ('Test2', ):
                self.assertIsInstance(itm, NavBarDropDownItem)
                for dd_itm in itm.items:
                    if hasattr(dd_itm, 'name') and dd_itm.name in ('Test3', 'Test4', 'Test5'):
                        if dd_itm.name == 'Test3':
                            with self.assertRaises(NoReverseMatch):
                                dd_itm.get_url()
                        elif dd_itm.name == 'Test4':
                            self.assertEqual(dd_itm.get_url(), 'javascript:void(0);')
                        self.assertIsInstance(dd_itm, NavBarLinkItem)
                    else:
                        self.assertIsInstance(dd_itm, NavBarDropDownDivider)


class PropellerCardTests(TestCase):
    def test_card_media(self):
        res = DemoMediaImage1().as_html()
        self.assertEqual('<img src="http://propeller.in/assets/images/profile-pic.png" class="img-responsive">', res)
        res = DemoMediaImage3().as_html()
        self.assertIsNone(res)
        res = DemoMedia1().as_html()
        self.assertEqual('<div class="pmd-card-media"><div class="media-body"></div></div>', res)
        res = DemoMedia2().as_html()
        self.assertEqual('<div class="pmd-card-media"><div class="media-body">'
                         '<img src="http://propeller.in/assets/images/profile-pic.png" class="img-responsive">'
                         '</div></div>', res)
        res = DemoMedia3().as_html()
        self.assertEqual('<div class="pmd-card-media"><div class="media-body"></div>'
                         '<div class="media-right media-middle">'
                         '<img src="http://propeller.in/assets/images/profile-pic.png" width="80" height="80">'
                         '</div></div>', res)

    def test_rendered_template(self):
        res = self.render_template_with_propeller(
            '{% propeller_card card1 %}',
            context={'card1': DemoCard1()}
        )
        self.assertInHTML(RESULT_CARD1, res)
        res = self.render_template_with_propeller(
            '{% propeller_card card2 %}',
            context={'card2': DemoCard2()}
        )
        self.assertInHTML(RESULT_CARD2, res)
        res = self.render_template_with_propeller(
            '{% propeller_card card3 %}', {'card3': DemoCard3()}
        )
        self.assertInHTML(RESULT_CARD3, res)
        res = self.render_template_with_propeller(
            '{% propeller_card card4 %}', {'card4': DemoCard4()}
        )
        self.assertInHTML(RESULT_CARD4, res)
        res = self.render_template_with_propeller(
            '{% propeller_card card5 %}', {'card5': DemoCard5()}
        )
        self.assertInHTML(RESULT_CARD5, res)

    def test_exceptions(self):
        with self.assertRaises(PropellerException):
            DemoMedia4().get_media_body()
        with self.assertRaises(PropellerException):
            DemoMedia5().get_media_body_inline()
