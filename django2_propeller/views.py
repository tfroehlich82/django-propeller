# -*- coding: utf-8 -*-
from django.views.generic.base import ContextMixin


class NavBarMixin(ContextMixin):
    navbar_class = None
    navbar_name = 'navbar'

    def get_context_data(self, **kwargs):
        context = super(NavBarMixin, self).get_context_data(**kwargs)
        context[self.navbar_name] = self.navbar_class
        return context
