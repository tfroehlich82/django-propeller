# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView, View, ContextMixin

from .forms import ContactForm, FilesForm, ContactFormSet
from django_propeller.navbar import NavBar, NavBarItem, NavBarDropDownItem


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class MyNavBar(NavBar):
    brandname = "django-propeller"
    items = [
        NavBarItem("Home", "home"),
        NavBarItem("Typography", "typo"),
        NavBarItem("Buttons", "buttons"),
        NavBarItem("Floating Action Buttons", "fabs"),
        NavBarDropDownItem("Forms", [
            NavBarItem("Form", "form_default"),
            NavBarItem("Formset", "formset_default"),
            NavBarItem("Form by field", "form_by_field"),
            NavBarItem("Form horizontal", "form_horizontal"),
            NavBarItem("Form inline", "form_inline"),
            NavBarItem("Form with files", "form_with_files"),
        ]),
        NavBarItem("Pagination", "pagination"),
        NavBarItem("Miscellaneous", "misc"),
    ]


class NavBarView(TemplateView):
    navbar = None

    def get_context_data(self, **kwargs):
        context = super(NavBarView, self).get_context_data(**kwargs)
        context['main_navbar'] = self.navbar
        return context


class HomePageView(NavBarView):
    template_name = 'home.html'
    navbar = MyNavBar()

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'hello http://example.com')
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


class PaginationView(NavBarView):
    template_name = 'pagination.html'
    navbar = MyNavBar()

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


class MiscView(NavBarView):
    template_name = 'misc.html'
    navbar = MyNavBar()


class ButtonsView(NavBarView):
    template_name = 'buttons.html'
    navbar = MyNavBar()


class FABsView(NavBarView):
    template_name = 'fabs.html'
    navbar = MyNavBar()


class TypoView(NavBarView):
    template_name = 'typo.html'
    navbar = MyNavBar()

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
