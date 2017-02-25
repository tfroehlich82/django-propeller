# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from django_propeller.views import NavBarMixin
from django_propeller_demo.navbars import MainNavBar, DemoNavBar1
from .forms import ContactForm, FilesForm, ContactFormSet


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class HomePageView(TemplateView, NavBarMixin):
    template_name = 'home.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        return context


class DefaultFormsetView(FormView, NavBarMixin):
    template_name = 'formset.html'
    form_class = ContactFormSet
    navbar_class = MainNavBar


class DefaultFormView(FormView, NavBarMixin):
    template_name = 'form.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class DefaultFormByFieldView(FormView, NavBarMixin):
    template_name = 'form_by_field.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class FormHorizontalView(FormView, NavBarMixin):
    template_name = 'form_horizontal.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class FormInlineView(FormView, NavBarMixin):
    template_name = 'form_inline.html'
    form_class = ContactForm
    navbar_class = MainNavBar


class FormWithFilesView(FormView, NavBarMixin):
    template_name = 'form_with_files.html'
    form_class = FilesForm
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }


class PaginationView(TemplateView, NavBarMixin):
    template_name = 'pagination.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(200):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView, NavBarMixin):
    template_name = 'misc.html'
    navbar_class = MainNavBar


class ButtonsView(TemplateView, NavBarMixin):
    template_name = 'buttons.html'
    navbar_class = MainNavBar


class FABsView(TemplateView, NavBarMixin):
    template_name = 'fabs.html'
    navbar_class = MainNavBar


class TypoView(TemplateView, NavBarMixin):
    template_name = 'typo.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(TypoView, self).get_context_data(**kwargs)
        context['text1'] = "Propeller Heading"
        context['text2'] = "with secondary heading"
        context['text3'] = "Really large heading"
        context['text4'] = "Larger heading"
        context['text5'] = "Large heading"
        context['text6'] = "Normal heading"
        context['text7'] = "Heading"
        context['text8'] = "Lead text..."
        context['text9'] = "Normal text..."
        context['text10'] = "With this filter you can "
        context['text11'] = "highlight some text"
        context['text12'] = "strikethrough some text"
        context['text13'] = "underline some text"
        context['text14'] = "show some bold text"
        context['text15'] = "show some italic text"
        return context


class NavBarView(TemplateView, NavBarMixin):
    template_name = 'navbar.html'
    navbar_class = MainNavBar

    def get_context_data(self, **kwargs):
        context = super(NavBarView, self).get_context_data(**kwargs)
        context['navbar1'] = DemoNavBar1
        return context
