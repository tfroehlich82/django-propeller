# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from .views import HomePageView, FormHorizontalView, FormInlineView, PaginationView, FormWithFilesView, \
    DefaultFormView, MiscView, DefaultFormsetView, DefaultFormByFieldView, ButtonsView, FABsView, TypoView, NavBarView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^typo$', TypoView.as_view(), name='typo'),
    url(r'^buttons$', ButtonsView.as_view(), name='buttons'),
    url(r'^fabs$', FABsView.as_view(), name='fabs'),
    url(r'^navbar$', NavBarView.as_view(), name='navbar'),
    url(r'^formset$', DefaultFormsetView.as_view(), name='formset_default'),
    url(r'^form$', DefaultFormView.as_view(), name='form_default'),
    url(r'^form_by_field$', DefaultFormByFieldView.as_view(), name='form_by_field'),
    url(r'^form_horizontal$', FormHorizontalView.as_view(), name='form_horizontal'),
    url(r'^form_inline$', FormInlineView.as_view(), name='form_inline'),
    url(r'^form_with_files$', FormWithFilesView.as_view(), name='form_with_files'),
    url(r'^pagination$', PaginationView.as_view(), name='pagination'),
    url(r'^misc$', MiscView.as_view(), name='misc'),
]
