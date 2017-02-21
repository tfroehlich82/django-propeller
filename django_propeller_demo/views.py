# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView

from .forms import ContactForm, FilesForm, ContactFormSet
from django_propeller.navbar import NavBar, NavBarItem


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


navbar = NavBar("This is a test", items=[
    NavBarItem("Test1"),
    NavBarItem("Test2"),
    NavBarItem("Test3"),
])


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
        context['mynavbar'] = navbar
        return context


class DefaultFormsetView(FormView):
    template_name = 'formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }


class PaginationView(TemplateView):
    template_name = 'pagination.html'

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


class MiscView(TemplateView):
    template_name = 'misc.html'


class ButtonsView(TemplateView):
    template_name = 'buttons.html'


class FABsView(TemplateView):
    template_name = 'fabs.html'


class TypoView(TemplateView):
    template_name = 'typo.html'

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
